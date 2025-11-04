from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils import timezone

from .models import User, SecurityPolicy, SecurityLog, SecurityConfig
from .forms import RegisterForm, LoginForm, OTPForm, Enable2FAConfirmForm, ChangePasswordForm
from .tokens import email_verification_token
from .otp_algo import generate_base32_secret, provisioning_uri, verify_totp
from .utils import qr_code_base64


def _log_event(user, event, request=None, note=""):
    SecurityLog.objects.create(
        user=user,
        event=event,
        ip=(request.META.get("REMOTE_ADDR", "") if request else ""),
        note=note,
        created_at=timezone.now(),
    )


def send_activation_email(request, user):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_verification_token.make_token(user)
    domain = (getattr(settings, "SITE_DOMAIN", "") or "").rstrip("/") or f"http://{request.get_host()}"
    activate_url = f"{domain}{reverse('accounts:activate', kwargs={'uidb64': uidb64, 'token': token})}"

    subject = f"Kích hoạt tài khoản - {getattr(settings, 'SITE_NAME', 'TwoFA Demo')}"
    message = (
        f"Xin chào {user.username},\n\n"
        f"Bạn vừa đăng ký tài khoản. Hãy nhấp liên kết sau để kích hoạt:\n{activate_url}\n\n"
        f"Nếu không phải bạn, vui lòng bỏ qua email này."
    )
    send_mail(subject, message, getattr(settings, "DEFAULT_FROM_EMAIL", None), [user.email], fail_silently=False)


def activate_email_view(request, uidb64, token):
    UserModel = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except Exception:
        user = None

    if user and email_verification_token.check_token(user, token):
        user.is_active = True
        if hasattr(user, "email_verified"):
            user.email_verified = True
        user.save()
        messages.success(request, "Kích hoạt tài khoản thành công. Vui lòng đăng nhập.")
        return redirect("accounts:login")
    else:
        messages.error(request, "Liên kết kích hoạt không hợp lệ hoặc đã hết hạn.")
        return redirect("accounts:register")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email_verified = False
            user.role = "USER"
            user.is_active = False  # bắt buộc kích hoạt qua email

            # Áp dụng SecurityPolicy nếu có (không làm app crash nếu model/DB chưa sẵn)
            must_setup_2fa = True
            try:
                policy = SecurityPolicy.objects.first()
                if policy:
                    must_setup_2fa = bool(getattr(policy, "require_2fa_for_new_users", True))
            except Exception:
                pass
            user.must_setup_2fa = must_setup_2fa

            user.save()

            # Gửi email kích hoạt
            try:
                send_activation_email(request, user)
            except Exception as e:
                messages.warning(request, f"Đăng ký thành công, nhưng gửi mail kích hoạt lỗi: {e}")

            messages.success(request, "Đăng ký thành công! Vui lòng kiểm tra email để kích hoạt tài khoản.")
            return redirect("accounts:login")

        return render(request, "accounts/register.html", {"form": form})

    form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    """
    Bước 1: đăng nhập bằng mật khẩu.
    - Nếu user đã bật 2FA => chuyển sang bước OTP.
    - Nếu chưa bật 2FA:
        * enforce_2fa_all=True => ép bật 2FA (login tạm để vào enable-2fa)
        * enforce_2fa_all=False => login bình thường; nếu must_setup_2fa=True vẫn ép enable-2fa
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]

            config = SecurityPolicy.objects.first()
            enforce_all = bool(getattr(config, "enforce_2fa_all", False))
            if user.is_staff or user.is_superuser:
                enforce_all = True

            if user.is_2fa_enabled:
                request.session["pre_2fa_user_id"] = user.id
                return redirect("accounts:otp_verify")

            # login tạm nếu cần ép enable-2fa
            login(request, user)
            _log_event(user, "LOGIN_SUCCESS", request=request, note="Login without 2FA yet")

            if enforce_all or (user.must_setup_2fa and not user.is_2fa_enabled):
                return redirect("accounts:enable_2fa")

            if user.must_change_password:
                return redirect("accounts:change_password")

            return redirect("accounts:dashboard")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


def otp_verify_view(request):
    """
    Bước 2: nhập OTP khi user.is_2fa_enabled == True
    """
    user_id = request.session.get("pre_2fa_user_id")
    if not user_id:
        return redirect("accounts:login")

    user = get_object_or_404(User, pk=user_id)

    if user.otp_locked:
        _log_event(user, "OTP_LOCKED", request=request, note="User tried while locked")
        return render(
            request,
            "accounts/otp_verify.html",
            {
                "form": OTPForm(),
                "username": user.username,
                "locked": True,
                "error": "Tài khoản đã bị khóa OTP do nhập sai quá nhiều lần. Liên hệ admin để mở khóa."
            },
            status=403,
        )

    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["otp_code"]
            ok = verify_totp(user.otp_secret, code, period=30, digits=6, algo="SHA1", window=1)
            if ok:
                user.failed_otp_attempts = 0
                user.otp_locked = False
                user.save()

                _log_event(user, "OTP_SUCCESS", request=request, note="OTP ok, full login")

                login(request, user)
                request.session.pop("pre_2fa_user_id", None)

                if user.must_setup_2fa and not user.is_2fa_enabled:
                    return redirect("accounts:enable_2fa")
                if user.must_change_password:
                    return redirect("accounts:change_password")
                return redirect("accounts:dashboard")
            else:
                user.failed_otp_attempts += 1
                note_msg = f"OTP failed attempt {user.failed_otp_attempts}"
                if user.failed_otp_attempts >= 5:
                    user.otp_locked = True
                    note_msg += " -> LOCKED"
                user.save()
                _log_event(user, "OTP_FAIL", request=request, note=note_msg)
                form.add_error("otp_code", "Mã OTP không hợp lệ.")
    else:
        form = OTPForm()

    return render(request, "accounts/otp_verify.html", {"form": form, "username": user.username})


@login_required
def enable_2fa_view(request):
    user = request.user

    if not user.otp_secret:
        user.otp_secret = generate_base32_secret()
        user.save()

    otp_uri = provisioning_uri(
        account_name=user.username,
        issuer_name=getattr(settings, "SITE_NAME", "TwoFA Demo"),
        secret_b32=user.otp_secret,
        algo="SHA1",
        digits=6,
        period=30,
    )
    qr_b64 = qr_code_base64(otp_uri)

    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["otp_code"]
            ok = verify_totp(user.otp_secret, code, period=30, digits=6, algo="SHA1", window=1)
            if ok:
                user.is_2fa_enabled = True
                user.failed_otp_attempts = 0
                user.otp_locked = False
                user.must_setup_2fa = False
                user.save()
                return redirect("accounts:dashboard")
            else:
                form.add_error("otp_code", "Mã OTP không hợp lệ.")
    else:
        form = OTPForm()

    return render(
        request,
        "accounts/enable_2fa.html",
        {
            "form": form,
            "qr_b64": qr_b64,
            "otp_uri": otp_uri,
            "is_enabled": user.is_2fa_enabled,
            "secret_key": user.otp_secret,
            "issuer": getattr(settings, "SITE_NAME", "TwoFA Demo"),
            "account_name": user.username,
            "digits": 6,
            "period": 30,
            "algo": "SHA1",
        },
    )


@login_required
def change_password_view(request):
    user = request.user
    if request.method == "POST":
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            new_pw = form.cleaned_data["new_password1"]
            user.set_password(new_pw)
            user.must_change_password = False
            user.save()
            login(request, user)
            return redirect("accounts:dashboard")
    else:
        form = ChangePasswordForm(user)
    return render(request, "accounts/change_password.html", {"form": form})


@login_required
def dashboard_view(request):
    u = request.user
    if u.must_setup_2fa and not u.is_2fa_enabled:
        return redirect("accounts:enable_2fa")
    if u.must_change_password:
        return redirect("accounts:change_password")

    security_info = {
        "email_verified": u.email_verified,
        "is_2fa_enabled": u.is_2fa_enabled,
        "must_setup_2fa": u.must_setup_2fa,
        "otp_locked": u.otp_locked,
        "failed_otp_attempts": u.failed_otp_attempts,
        "must_change_password": u.must_change_password,
        "last_login": u.last_login,
    }
    return render(request, "accounts/dashboard.html", {"security_info": security_info})


def logout_view(request):
    logout(request)
    return redirect("forum:home")


@login_required
def staff_only_view(request):
    if not request.user.is_staff_role():
        return HttpResponseForbidden("Bạn không có quyền STAFF.")
    return render(request, "accounts/dashboard.html", {"staff": True})
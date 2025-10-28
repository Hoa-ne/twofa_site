from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils import timezone

from .models import User, SecurityPolicy, SecurityLog
from .forms import RegisterForm, LoginForm, OTPForm, Enable2FAConfirmForm, ChangePasswordForm
from .tokens import email_verification_token
from .utils import create_otp_secret, build_totp_uri, qr_code_base64, verify_totp


def _log_event(user, event, request=None, note=""):
    SecurityLog.objects.create(
        user=user,
        event=event,
        ip=(request.META.get("REMOTE_ADDR", "") if request else ""),
        note=note,
        created_at=timezone.now(),
    )


def send_verification_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_verification_token.make_token(user)
    activation_link = f"{settings.SITE_DOMAIN}{reverse('accounts:activate', args=[uid, token])}"

    subject = "[TwoFA Demo] Xác nhận email"
    message = (
        f"Chào {user.username},\n"
        f"Bấm link sau để kích hoạt tài khoản:\n{activation_link}\n"
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email_verified = False
            user.role = "USER"

            # Áp dụng SecurityPolicy cho user mới
            policy = SecurityPolicy.objects.first()
            if policy:
                user.must_setup_2fa = policy.require_2fa_for_new_users
            else:
                user.must_setup_2fa = True  # fallback: bắt buộc 2FA

            # user vừa tạo thì chưa bật 2FA, chưa có otp_secret
            # must_change_password mặc định False
            user.save()

            send_verification_email(request, user)

            return render(request, "accounts/verify_email_sent.html", {"email": user.email})
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def activate_email_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user and email_verification_token.check_token(user, token):
        user.email_verified = True
        user.save()
        return render(request, "accounts/activate_success.html", {"ok": True})
    return render(request, "accounts/activate_success.html", {"ok": False})


def login_view(request):
    """
    Logic login (bước 1: mật khẩu):
    1. Kiểm tra username/password và email_verified.
    2. Nếu user.is_2fa_enabled == True:
          -> KHÔNG login ngay
          -> Lưu pre_2fa_user_id và chuyển sang otp_verify_view
          -> Nếu user.otp_locked == True thì vẫn chuyển, nhưng otp_verify_view sẽ báo khóa.
    3. Nếu user.is_2fa_enabled == False:
          -> login() tạm
          -> Nếu user.must_setup_2fa == True: ép sang enable_2fa_view
          -> else nếu user.must_change_password == True: ép sang change_password_view
          -> else vào dashboard
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]

            # User đã bật 2FA -> cần OTP bước 2
            if user.is_2fa_enabled:
                request.session["pre_2fa_user_id"] = user.id
                return redirect("accounts:otp_verify")

            # User CHƯA bật 2FA
            login(request, user)
            _log_event(user, "LOGIN_SUCCESS", request=request, note="Login without 2FA yet")

            # Nếu bị ép setup 2FA ngay
            if user.must_setup_2fa and not user.is_2fa_enabled:
                return redirect("accounts:enable_2fa")

            # Nếu bị ép đổi mật khẩu
            if user.must_change_password:
                return redirect("accounts:change_password")

            return redirect("accounts:dashboard")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


def otp_verify_view(request):
    """
    Bước 2 của login khi user.is_2fa_enabled == True.
    - Nếu tài khoản bị otp_locked => chặn luôn.
    - Nếu OTP sai: tăng failed_otp_attempts, nếu >=5 thì otp_locked=True.
    - Nếu OTP đúng:
        + reset failed_otp_attempts, otp_locked=False
        + login() chính thức
        + sau đó kiểm tra must_setup_2fa / must_change_password giống dashboard logic.
    """
    user_id = request.session.get("pre_2fa_user_id")
    if not user_id:
        return redirect("accounts:login")

    user = get_object_or_404(User, pk=user_id)

    # nếu đã bị khóa OTP thì từ chối luôn
    if user.otp_locked:
        _log_event(user, "OTP_LOCKED", request=request, note="User tried while locked")
        return render(
            request,
            "accounts/otp_verify.html",
            {
                "form": OTPForm(),
                "username": user.username,
                "locked": True,
                "error": "Tài khoản của bạn đã bị khóa OTP do nhập sai quá nhiều lần. Liên hệ admin để mở khóa."
            },
            status=403,
        )

    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["otp_code"]

            if verify_totp(user, code):
                # OTP đúng
                user.failed_otp_attempts = 0
                user.otp_locked = False
                user.save()

                _log_event(user, "OTP_SUCCESS", request=request, note="OTP ok, full login")

                login(request, user)
                request.session.pop("pre_2fa_user_id", None)

                # ép setup 2FA? (trong thực tế is_2fa_enabled True rồi, nên thường không)
                if user.must_setup_2fa and not user.is_2fa_enabled:
                    return redirect("accounts:enable_2fa")

                # ép đổi mật khẩu?
                if user.must_change_password:
                    return redirect("accounts:change_password")

                return redirect("accounts:dashboard")
            else:
                # OTP sai
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
    """
    Trang này cho user quét QR và confirm OTP để bật 2FA.
    - Nếu user chưa có otp_secret -> tạo mới.
    - Khi xác nhận OTP thành công:
        is_2fa_enabled = True
        must_setup_2fa = False
    """
    user = request.user

    if not user.otp_secret:
        user.otp_secret = create_otp_secret()
        user.save()

    otp_uri = build_totp_uri(user)
    qr_b64 = qr_code_base64(otp_uri)

    if request.method == "POST":
        form = Enable2FAConfirmForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["otp_code"]
            if verify_totp(user, code):
                user.is_2fa_enabled = True
                user.must_setup_2fa = False
                user.save()
                _log_event(user, "OTP_SUCCESS", request=request, note="Enable 2FA success")
                return redirect("accounts:dashboard")
            else:
                form.add_error("otp_code", "Mã OTP sai. Thử lại.")
    else:
        form = Enable2FAConfirmForm()

    ctx = {
        "qr_b64": qr_b64,
        "otp_uri": otp_uri,
        "is_enabled": user.is_2fa_enabled,
        "form": form,
    }
    return render(request, "accounts/enable_2fa.html", ctx)


@login_required
def change_password_view(request):
    """
    Nếu user.must_change_password == True thì ép người dùng đổi mật khẩu.
    Sau khi đổi xong:
       - set_password()
       - must_change_password = False
       - login lại (để refresh session)
    """
    user = request.user

    if request.method == "POST":
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            new_pw = form.cleaned_data["new_password1"]
            user.set_password(new_pw)
            user.must_change_password = False
            user.save()
            # login lại với mật khẩu mới
            login(request, user)
            return redirect("accounts:dashboard")
    else:
        form = ChangePasswordForm(user)

    return render(request, "accounts/change_password.html", {"form": form})


@login_required
def dashboard_view(request):
    """
    Dashboard user:
    - Nếu must_setup_2fa=True và user chưa bật 2FA -> ép đến enable_2fa_view
    - Nếu must_change_password=True -> ép đến change_password_view
    - Nếu otp_locked=True -> cảnh báo
    Hiển thị trạng thái bảo mật cho user.
    """
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

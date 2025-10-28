from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from .models import User
from .forms import RegisterForm, LoginForm, OTPForm, Enable2FAConfirmForm
from .tokens import email_verification_token
from .utils import create_otp_secret, build_totp_uri, qr_code_base64, verify_totp

from .models import User, SecurityPolicy

# --- Đăng ký & kích hoạt email (không đổi nhiều) ---

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email_verified = False
            user.role = "USER"

            # --- TOÀN BỘ KHỐI NÀY CẦN ĐƯỢC THỤT LỀ VÀO TRONG ---
            # Áp dụng chính sách toàn hệ thống:
            policy = SecurityPolicy.objects.first()
            if policy:
                # Nếu admin KHÔNG bắt buộc 2FA cho user mới
                if policy.require_2fa_for_new_users is False:
                    user.must_setup_2fa = False
                else:
                    user.must_setup_2fa = True
            else:
                # fallback: nếu chưa có policy trong DB thì cứ bắt buộc
                user.must_setup_2fa = True

            # is_2fa_enabled mặc định False, otp_secret chưa có
            user.save()

            send_verification_email(request, user)

            return render(request, "accounts/verify_email_sent.html", {"email": user.email})
        # --- KẾT THÚC KHỐI CẦN THỤT LỀ ---
        
        # Khối 'else' này cũng cần được sửa thụt lề để ngang hàng với 'if form.is_valid():'
        # Nó sẽ render lại trang register với các lỗi validation
        else:
            return render(request, "accounts/register.html", {"form": form})
            
    # 'else' này ngang hàng với 'if request.method == "POST":'
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})

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


# --- Đăng nhập & xử lý 2FA logic mới ---

def login_view(request):
    """
    Logic:
    1. Kiểm tra username/password + email_verified.
    2. Nếu user.is_2fa_enabled == True:
        -> chưa login ngay
        -> chuyển sang bước OTP (/accounts/otp/)
    3. Nếu user.is_2fa_enabled == False:
        3a. login(request, user) tạm
        3b. nếu user.must_setup_2fa == True:
                redirect đến /accounts/enable-2fa/ để buộc scan QR và bật 2FA
            else:
                vào dashboard luôn
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]

            # Trường hợp user đã bật 2FA => bắt OTP
            if user.is_2fa_enabled:
                request.session["pre_2fa_user_id"] = user.id
                return redirect("accounts:otp_verify")

            # User chưa bật 2FA
            login(request, user)

            # Nếu admin ép phải setup 2FA ngay
            if user.must_setup_2fa and not user.is_2fa_enabled:
                return redirect("accounts:enable_2fa")

            # Nếu không bị ép, cho vào dashboard bình thường
            return redirect("accounts:dashboard")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


def otp_verify_view(request):
    """
    Cho user đã bật 2FA:
    - Sau khi password đúng, ta lưu pre_2fa_user_id trong session.
    - User nhập OTP 6 số, nếu đúng thì login() chính thức và vào dashboard.
    """
    user_id = request.session.get("pre_2fa_user_id")
    if not user_id:
        return redirect("accounts:login")

    user = get_object_or_404(User, pk=user_id)

    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["otp_code"]
            if verify_totp(user, code):
                # OTP hợp lệ -> login chính thức
                login(request, user)
                request.session.pop("pre_2fa_user_id", None)

                # Trong trường hợp admin vẫn để must_setup_2fa=True (hiếm)
                # ta vẫn ép họ đi bật 2FA lại nếu cần
                if user.must_setup_2fa and not user.is_2fa_enabled:
                    return redirect("accounts:enable_2fa")

                return redirect("accounts:dashboard")
            else:
                form.add_error("otp_code", "Mã OTP không hợp lệ")
    else:
        form = OTPForm()

    return render(request, "accounts/otp_verify.html", {"form": form, "username": user.username})


@login_required
def enable_2fa_view(request):
    user = request.user

    # Nếu user đã bật 2FA rồi -> KHÔNG lộ secret nữa
    if user.is_2fa_enabled:
        return render(
            request,
            "accounts/enable_2fa.html",
            {
                "is_enabled": True,
                "qr_b64": None,
                "otp_uri": None,
                "show_form": False,  # template sẽ dùng flag này để ẩn form/QR
            },
        )

    # Nếu user CHƯA bật 2FA:
    # 1. Đảm bảo có secret
    if not user.otp_secret:
        user.otp_secret = create_otp_secret()
        user.save()

    # 2. Tạo QR và URI để hiển thị
    otp_uri = build_totp_uri(user)
    qr_b64 = qr_code_base64(otp_uri)

    if request.method == "POST":
        code = request.POST.get("otp_code", "").strip()
        if verify_totp(user, code):
            # OTP nhập đúng -> bật 2FA
            user.is_2fa_enabled = True
            user.must_setup_2fa = False
            user.save()
            messages.success(request, "Đã kích hoạt 2FA cho tài khoản của bạn.")
            return redirect("accounts:enable_2fa")  # reload trang ở trạng thái enabled
        else:
            messages.error(request, "Mã OTP không hợp lệ. Vui lòng thử lại.")

    return render(
        request,
        "accounts/enable_2fa.html",
        {
            "is_enabled": False,
            "qr_b64": qr_b64,
            "otp_uri": otp_uri,
            "show_form": True,  # cho template biết có form nhập OTP
        },
    )


@login_required
def dashboard_view(request):
    """
    Dashboard. Tuy nhiên nếu must_setup_2fa vẫn True và user chưa bật 2FA,
    chặn họ ra ngoài luôn: ép vào trang enable_2fa.
    """
    u = request.user
    if u.must_setup_2fa and not u.is_2fa_enabled:
        # ép quét OTP trước khi dùng hệ thống
        return redirect("accounts:enable_2fa")

    return render(request, "accounts/dashboard.html")


def logout_view(request):
    logout(request)
    return redirect("forum:home")


@login_required
def staff_only_view(request):
    if not request.user.is_staff_role():
        return HttpResponseForbidden("Bạn không có quyền STAFF.")
    return render(request, "accounts/dashboard.html", {"staff": True})


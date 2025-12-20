from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils import timezone
from datetime import timedelta
from .forms import ProfileEditForm
from django.core.paginator import Paginator
from collections import defaultdict, Counter
from django.db.models import Count
from datetime import timedelta

# Import decorator của ratelimit
from django_ratelimit.decorators import ratelimit

from .models import User, SecurityPolicy, SecurityLog, SecurityConfig
from .forms import (
    RegisterForm, LoginForm, OTPForm, Enable2FAConfirmForm,
    ChangePasswordForm, BackupCodeForm, Disable2FAForm
)
from .tokens import email_verification_token
from .otp_algo import (
    generate_base32_secret, provisioning_uri, verify_totp,
    qr_code_base64
)
from django.db.models import Count, F
from django.db.models.functions import TruncDate
import time
import secrets
import hmac

# --- 1. HÀM LẤY IP THỰC TẾ CỦA CLIENT ---

def get_client_ip(request):
    """Lấy địa chỉ IP thực của client (kể cả đi qua Proxy / Load Balancer)."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def ip_key_wrapper(group, request):
    """Hàm wrapper sử dụng IP làm key cho ratelimit."""
    return get_client_ip(request)


# --- 2. HÀM TẠO KEY RÀNG BUỘC IP + TÊN ĐĂNG NHẬP ---

def get_ratelimit_key(group, request):
    """
    Key giới hạn tần suất linh hoạt: kết hợp IP và tên đăng nhập.

    - Mục đích: Nếu một người dùng bị chặn thì không ảnh hưởng tới người dùng khác
      đang dùng chung mạng / cùng IP.
    """
    ip = get_client_ip(request)
    username = ""

    # Trường hợp 1: Người dùng đã đăng nhập (ví dụ: đổi mật khẩu, tắt 2FA)
    if request.user.is_authenticated:
        username = request.user.username

    # Trường hợp 2: Đang trong bước nhập OTP/Backup (chưa login hoàn toàn, lưu trong session)
    elif "pre_2fa_user_id" in request.session:
        try:
            uid = request.session["pre_2fa_user_id"]
            user = User.objects.get(pk=uid)
            username = user.username
        except User.DoesNotExist:
            username = "unknown"

    # Trường hợp 3: Đang gửi form đăng nhập (lấy username từ POST)
    elif request.method == "POST" and "username" in request.POST:
        username = request.POST.get("username", "").strip()

    # Nếu không xác định được username (ví dụ chỉ load trang GET), chỉ dùng IP
    if not username:
        return ip

    # Trả về key kết hợp, ví dụ: "192.168.1.1-admin"
    return f"{ip}-{username}"


def record_security_event(user, event_type, request=None, note=""):
    """Ghi log sự kiện bảo mật (login, OTP sai, bật/tắt 2FA, v.v.)."""
    user_ip = get_client_ip(request) if request else ""
    ua_string = ""
    if request:
        ua_string = request.META.get('HTTP_USER_AGENT', "")[:255]

    SecurityLog.objects.create(
        user=user,
        event_type=event_type,
        ip=user_ip,
        user_agent=ua_string,
        note=note,
        created_at=timezone.now(),
    )


def _set_session_expiry(request, remember_me: bool):
    """Thiết lập thời hạn session (ghi nhớ đăng nhập hoặc chỉ cho tới khi đóng trình duyệt)."""
    if remember_me:
        expiry_seconds = getattr(settings, "SESSION_COOKIE_AGE", 2592000)
        request.session.set_expiry(expiry_seconds)
    else:
        # 0 = hết phiên khi đóng trình duyệt
        request.session.set_expiry(0)


def _perform_login(request, user, remember_me: bool):
    """
    Thực hiện đăng nhập hoàn chỉnh sau khi đã qua tất cả bước kiểm tra (OTP, 2FA, v.v.).
    """
    _set_session_expiry(request, remember_me)

    # Đánh dấu thiết bị tin cậy nếu người dùng chọn nhớ
    if remember_me:
        request.session['2fa_trusted'] = True
        request.session['2fa_trusted_user_id'] = user.id
    else:
        request.session.pop('2fa_trusted', None)
        request.session.pop('2fa_trusted_user_id', None)

    login(request, user)
    request.session.pop("pre_2fa_user_id", None)

    # Nếu bị yêu cầu bắt buộc bật 2FA hoặc đổi mật khẩu thì điều hướng sang đó
    if user.must_setup_2fa and not user.is_2fa_enabled:
        return redirect("accounts:enable_2fa")
    if user.must_change_password:
        return redirect("accounts:change_password")
    return redirect("accounts:dashboard")


def send_activation_email(request, user):
    """Gửi email kích hoạt tài khoản cho người dùng mới đăng ký."""
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
    """Xử lý liên kết kích hoạt tài khoản gửi qua email."""
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
    """Đăng ký tài khoản mới, gửi email kích hoạt."""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email_verified = False
            user.role = "USER"
            user.is_active = False

            # Kiểm tra chính sách: có bắt buộc bật 2FA cho user mới không
            must_setup_2fa = True
            try:
                policy = SecurityPolicy.objects.first()
                if policy:
                    must_setup_2fa = bool(getattr(policy, "require_2fa_for_new_users", True))
            except Exception:
                pass
            user.must_setup_2fa = must_setup_2fa

            user.save()

            try:
                send_activation_email(request, user)
            except Exception as e:
                messages.warning(request, f"Đăng ký thành công, nhưng gửi mail kích hoạt lỗi: {e}")

            messages.success(request, "Đăng ký thành công! Vui lòng kiểm tra email để kích hoạt tài khoản.")
            return redirect("accounts:login")

        return render(request, "accounts/register.html", {"form": form})

    form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


# Dùng key=get_ratelimit_key để giới hạn theo cặp IP - tên đăng nhập
@ratelimit(key=get_ratelimit_key, rate='10/m', block=True)
def login_view(request):
    """
    View đăng nhập:
    - Có giới hạn tần suất theo cặp (IP - tên đăng nhập).
    - Xử lý logic bắt buộc 2FA / thiết bị tin cậy.
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]

            policy = SecurityPolicy.objects.first()
            config = SecurityConfig.get_solo()

            enforce_all = bool(getattr(policy, "require_2fa_for_new_users", True))
            if user.is_staff or user.is_superuser:
                enforce_all = True

            # Trường hợp hệ thống cấu hình BẮT BUỘC 2FA
            if config.enforce_2fa:
                # Người dùng chưa bật 2FA -> ép bật
                if not user.is_2fa_enabled:
                    login(request, user)
                    request.session.pop("pre_2fa_user_id", None)
                    messages.warning(
                        request,
                        "Hệ thống đang yêu cầu BẮT BUỘC 2FA. Vui lòng kích hoạt 2FA."
                    )
                    request.session.pop('2fa_trusted', None)
                    request.session.pop('2fa_trusted_user_id', None)
                    return redirect("accounts:enable_2fa")

                # Người dùng đã bật 2FA, nhưng thiết bị đã đánh dấu tin cậy
                if request.session.get('2fa_trusted', False) and \
                   request.session.get('2fa_trusted_user_id') == user.id:

                    record_security_event(
                        user,
                        "LOGIN_SUCCESS",
                        request=request,
                        note="Đăng nhập thành công (Thiết bị tin cậy)"
                    )
                    return _perform_login(request, user, True)

                # Cần bước OTP
                request.session["pre_2fa_user_id"] = user.id
                return redirect("accounts:otp_verify")

            # Trường hợp 2FA không bắt buộc toàn hệ thống nhưng user đã bật 2FA
            if user.is_2fa_enabled:
                if request.session.get('2fa_trusted', False) and \
                   request.session.get('2fa_trusted_user_id') == user.id:

                    record_security_event(
                        user,
                        "LOGIN_SUCCESS",
                        request=request,
                        note="Đăng nhập thành công (Thiết bị tin cậy)"
                    )
                    return _perform_login(request, user, True)

                request.session["pre_2fa_user_id"] = user.id
                return redirect("accounts:otp_verify")

            # Không bật 2FA: đăng nhập bình thường
            remember_me = False
            record_security_event(
                user,
                "LOGIN_SUCCESS",
                request=request,
                note="Đăng nhập không dùng 2FA"
            )
            return _perform_login(request, user, remember_me)
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


# Dùng key=get_ratelimit_key cho bước xác thực OTP
@ratelimit(key=get_ratelimit_key, rate='10/m', block=True)
def otp_verify_view(request):
    """View nhập mã OTP (TOTP hoặc OTP email)."""
    user_id = request.session.get("pre_2fa_user_id")
    if not user_id:
        return redirect("accounts:login")

    user = get_object_or_404(User, pk=user_id)
    config = SecurityConfig.get_solo()

    # Tài khoản đang bị khóa OTP
    if user.otp_locked:
        record_security_event(
            user,
            "OTP_LOCKED",
            request=request,
            note="Người dùng cố gắng xác thực khi OTP đã bị khóa"
        )
        return render(
            request,
            "accounts/otp_verify.html",
            {
                "form": OTPForm(),
                "username": user.username,
                "locked": True,
                "error": f"Tài khoản đã bị khóa OTP do nhập sai quá {config.lockout_threshold} lần. Liên hệ admin."
            },
            status=403,
        )

    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["otp_code"].strip().replace(" ", "")
            remember_me = form.cleaned_data.get("remember_me", False)

            totp_ok = False
            email_ok = False

            # Kiểm tra OTP TOTP
            if user.otp_secret:
                totp_ok = verify_totp(
                    user.otp_secret,
                    code,
                    period=30,
                    digits=6,
                    algo="SHA1",
                    window=1
                )

            # Kiểm tra OTP gửi qua email
            email_otp_code = request.session.get('email_otp_code')
            email_otp_expiry = request.session.get('email_otp_expiry', 0)

            if email_otp_code and hmac.compare_digest(code, email_otp_code) and time.time() < email_otp_expiry:
                email_ok = True
                request.session.pop('email_otp_code', None)
                request.session.pop('email_otp_expiry', None)

            if totp_ok or email_ok:
                # Reset đếm sai và trạng thái khóa
                user.failed_otp_attempts = 0
                user.otp_locked = False
                user.save()

                note = "OTP (TOTP) hợp lệ" if totp_ok else "OTP (Email) hợp lệ"
                record_security_event(
                    user,
                    "OTP_SUCCESS",
                    request=request,
                    note=f"{note}, đăng nhập hoàn chỉnh"
                )

                return _perform_login(request, user, remember_me)
            else:
                # Sai OTP
                user.failed_otp_attempts += 1
                note_msg = f"Nhập sai OTP lần thứ {user.failed_otp_attempts}"

                # Khóa nếu vượt ngưỡng
                if user.failed_otp_attempts >= config.lockout_threshold:
                    user.otp_locked = True
                    note_msg += " -> TÀI KHOẢN BỊ KHÓA OTP"
                user.save()
                record_security_event(user, "OTP_FAIL", request=request, note=note_msg)
                form.add_error("otp_code", "Mã OTP không hợp lệ hoặc đã hết hạn.")
    else:
        form = OTPForm()

    return render(
        request,
        "accounts/otp_verify.html",
        {
            "form": form,
            "username": user.username,
            "lockout_threshold": config.lockout_threshold
        }
    )


# Email vẫn dùng key theo IP (get_client_ip) để chặn spam từ một máy
@ratelimit(key=ip_key_wrapper, rate='2/m', block=True)
def send_email_otp_view(request):
    """Gửi mã OTP qua email trong bước xác thực 2FA."""
    user_id = request.session.get("pre_2fa_user_id")
    if not user_id:
        return redirect("accounts:login")

    user = get_object_or_404(User, pk=user_id)
    if not user.allow_email_otp:
        messages.error(
            request,
            "Tính năng nhận mã qua Email đã bị Admin TẮT đối với tài khoản này. Vui lòng sử dụng ứng dụng xác thực."
        )
        return redirect("accounts:otp_verify")

    # Chặn gửi liên tục trong vòng 60 giây
    last_sent = request.session.get('last_email_otp_sent', 0)
    if time.time() - last_sent < 60:
        messages.warning(request, "Vui lòng đợi 60 giây trước khi gửi lại mã.")
        return redirect("accounts:otp_verify")

    # Tạo mã 6 chữ số ngẫu nhiên
    code = str(secrets.randbelow(900000) + 100000)

    # Lưu vào session để kiểm tra
    request.session['email_otp_code'] = code
    request.session['email_otp_expiry'] = int(time.time()) + 300  # 5 phút
    request.session['last_email_otp_sent'] = int(time.time())

    try:
        subject = f"Mã xác thực 2FA - {getattr(settings, 'SITE_NAME', 'TwoFA Demo')}"
        message = (
            f"Mã xác thực 2FA của bạn là: {code}\n\n"
            f"Mã này có hiệu lực trong 5 phút.\n"
        )
        send_mail(
            subject,
            message,
            getattr(settings, "DEFAULT_FROM_EMAIL", None),
            [user.email],
            fail_silently=False
        )

        record_security_event(user, "EMAIL_OTP_SENT", request=request)
        messages.success(request, f"Đã gửi mã OTP đến email {user.email}.")
    except Exception as e:
        messages.error(request, f"Lỗi khi gửi email: {e}")

    return redirect("accounts:otp_verify")


# Dùng key=get_ratelimit_key cho xác thực mã khôi phục
@ratelimit(key=get_ratelimit_key, rate='10/m', block=True)
def backup_code_verify_view(request):
    """View nhập mã khôi phục (backup code) để đăng nhập khi mất OTP."""
    user_id = request.session.get("pre_2fa_user_id")
    if not user_id:
        return redirect("accounts:login")

    user = get_object_or_404(User, pk=user_id)
    config = SecurityConfig.get_solo()

    if user.otp_locked:
        return render(
            request, "accounts/backup_code_verify.html",
            {
                "form": BackupCodeForm(),
                "username": user.username,
                "locked": True,
                "error": f"Tài khoản đã bị khóa OTP do nhập sai quá {config.lockout_threshold} lần. Liên hệ admin."
            },
            status=403,
        )

    if request.method == "POST":
        form = BackupCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"].strip()
            remember_me = form.cleaned_data.get("remember_me", False)

            if user.verify_backup_code(code):
                user.failed_otp_attempts = 0
                user.otp_locked = False
                user.save()

                record_security_event(
                    user,
                    "BACKUP_CODE_USED",
                    request=request,
                    note="Đăng nhập thành công (Mã khôi phục)"
                )

                return _perform_login(request, user, remember_me)
            else:
                user.failed_otp_attempts += 1
                note_msg = f"Nhập sai mã khôi phục lần thứ {user.failed_otp_attempts}"

                if user.failed_otp_attempts >= config.lockout_threshold:
                    user.otp_locked = True
                    note_msg += " -> TÀI KHOẢN BỊ KHÓA OTP"
                user.save()
                record_security_event(user, "OTP_FAIL", request=request, note=note_msg)
                form.add_error("code", "Mã khôi phục không hợp lệ hoặc đã được sử dụng.")
    else:
        form = BackupCodeForm()

    return render(
        request,
        "accounts/backup_code_verify.html",
        {"form": form, "username": user.username}
    )


@login_required
def enable_2fa_view(request):
    """View bật 2FA: sinh secret, hiển thị QR, yêu cầu nhập OTP để xác nhận."""
    user = request.user

    # Nếu chưa có secret thì sinh mới
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
            ok = verify_totp(
                user.otp_secret,
                code,
                period=30,
                digits=6,
                algo="SHA1",
                window=1
            )

            if ok:
                user.is_2fa_enabled = True
                user.failed_otp_attempts = 0
                user.otp_locked = False
                user.must_setup_2fa = False
                user.save()

                record_security_event(
                    user,
                    "ENABLE_2FA",
                    request=request,
                    note="Người dùng bật 2FA (TOTP)"
                )

                # Sinh mã khôi phục dạng plaintext và lưu tạm vào session để hiển thị 1 lần
                plaintext_codes = user.generate_backup_codes()
                request.session['backup_codes'] = plaintext_codes

                return redirect("accounts:enable_2fa_complete")
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
def enable_2fa_complete_view(request):
    """Hiển thị danh sách mã khôi phục sau khi bật 2FA lần đầu."""
    backup_codes = request.session.pop('backup_codes', None)
    if not backup_codes:
        return redirect("accounts:dashboard")

    return render(
        request,
        "accounts/enable_2fa_complete.html",
        {"backup_codes": backup_codes}
    )


# Đổi mật khẩu, có giới hạn tần suất theo IP + username
@login_required
@ratelimit(key=get_ratelimit_key, rate='10/m', block=True)
def change_password_view(request):
    """Cho phép người dùng tự đổi mật khẩu của chính mình."""
    user = request.user
    if request.method == "POST":
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            new_pw = form.cleaned_data["new_password1"]
            user.set_password(new_pw)
            user.must_change_password = False
            user.save()

            record_security_event(
                user,
                "PASSWORD_CHANGED",
                request=request,
                note="Người dùng tự đổi mật khẩu"
            )

            # Sau khi đổi mật khẩu, đăng nhập lại
            login(request, user)
            return redirect("accounts:dashboard")
    else:
        form = ChangePasswordForm(user)
    return render(request, "accounts/change_password.html", {"form": form})


@login_required
def dashboard_view(request):
    """Trang tổng quan tài khoản: trạng thái 2FA, email, khóa OTP, v.v."""
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
    """Đăng xuất, đồng thời xóa trạng thái thiết bị tin cậy."""
    request.session.pop('2fa_trusted', None)
    request.session.pop('2fa_trusted_user_id', None)
    logout(request)
    return redirect("forum:home")


@login_required
def staff_only_view(request):
    """View chỉ dành cho tài khoản có vai trò STAFF."""
    if not request.user.is_staff_role():
        return HttpResponseForbidden("Bạn không có quyền STAFF.")
    return render(request, "accounts/dashboard.html", {"staff": True})


@login_required
def profile_edit_view(request):
    """Chỉnh sửa hồ sơ cá nhân (thông tin, avatar...)."""
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật hồ sơ thành công!")
            return redirect("accounts:profile_view", pk=request.user.pk)
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, "accounts/profile_edit.html", {"form": form})


def profile_view(request, pk):
    """Xem trang hồ sơ cá nhân và bài viết của một người dùng."""
    profile_user = get_object_or_404(User, pk=pk)

    post_list = profile_user.post_set.all().order_by("-created_at")
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "profile_user": profile_user,
        "page_obj": page_obj
    }
    return render(request, "accounts/profile_view.html", context)


# Tắt 2FA – có giới hạn tần suất
@login_required
@ratelimit(key=get_ratelimit_key, rate='10/m', block=True)
def disable_2fa_view(request):
    """Cho phép người dùng tự tắt 2FA (sau khi xác thực lại OTP)."""
    user = request.user
    if not user.is_2fa_enabled:
        messages.error(request, "2FA chưa được bật.")
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = Disable2FAForm(user, request.POST)
        if form.is_valid():
            code = form.cleaned_data["otp_code"]
            ok = verify_totp(
                user.otp_secret,
                code,
                period=30,
                digits=6,
                algo="SHA1",
                window=1
            )

            if ok:
                user.is_2fa_enabled = False
                user.otp_secret = None
                user.failed_otp_attempts = 0
                user.otp_locked = False
                user.save()

                # Xóa toàn bộ mã khôi phục
                user.backup_codes.all().delete()

                record_security_event(
                    user,
                    "DISABLE_2FA",
                    request=request,
                    note="Người dùng tự tắt 2FA"
                )
                messages.success(request, "Xác thực hai lớp (2FA) đã được tắt.")
                return redirect("accounts:dashboard")
            else:
                form.add_error("otp_code", "Mã OTP không hợp lệ.")
    else:
        form = Disable2FAForm(user)

    return render(request, "accounts/disable_2fa.html", {"form": form})


def ratelimited_error_view(request, exception=None):
    """Trang hiển thị khi người dùng bị chặn do vượt giới hạn ratelimit."""
    return render(request, 'ratelimited.html', status=403)


def _simplify_user_agent(ua_string):
    """
    Rút gọn chuỗi User-Agent thành dạng dễ đọc, gom nhóm theo hệ điều hành + trình duyệt.
    """
    if not ua_string or ua_string == "Unknown":
        return "Không xác định"

    ua = ua_string.lower()

    os = "Khác"
    if "windows" in ua:
        os = "Windows"
    elif "mac os" in ua:
        os = "macOS"
    elif "android" in ua:
        os = "Android"
    elif "iphone" in ua or "ipad" in ua:
        os = "iOS"
    elif "linux" in ua:
        os = "Linux"

    browser = "Trình duyệt"
    if "edg" in ua:
        browser = "Edge"
    elif "chrome" in ua:
        browser = "Chrome"
    elif "firefox" in ua:
        browser = "Firefox"
    elif "safari" in ua:
        browser = "Safari"
    elif "opera" in ua or "opr" in ua:
        browser = "Opera"

    return f"{os} ({browser})"


@login_required
def security_dashboard_view(request):
    """
    Trang tổng quan bảo mật cho STAFF:
    - Thống kê 2FA, số lần sai OTP, tài khoản bị khóa,
    - Biểu đồ sai OTP 7 ngày gần đây,
    - Top thiết bị đăng nhập (User-Agent đã rút gọn).
    """
    if not request.user.is_staff_role():
        return HttpResponseForbidden("Bạn không có quyền truy cập.")

    # 1. Các chỉ số tổng quan
    total_users = User.objects.count()
    users_2fa_on = User.objects.filter(is_2fa_enabled=True).count()
    users_2fa_off = total_users - users_2fa_on
    otp_locked_count = User.objects.filter(otp_locked=True).count()
    total_otp_fails = SecurityLog.objects.filter(event_type='OTP_FAIL').count()

    # 2. Xử lý biểu đồ "Số lần nhập sai OTP (7 ngày qua)"
    # Cách mới: tính toán bằng Python để tránh lỗi timezone / giá trị null

    last_7_days = timezone.now() - timedelta(days=7)

    # Lấy dữ liệu thô từ DB
    logs = SecurityLog.objects.filter(event_type='OTP_FAIL', created_at__gte=last_7_days)

    # Gom nhóm số lần nhập sai theo ngày (dạng dd/mm)
    data_map = defaultdict(int)

    for log in logs:
        # Chuyển về giờ Việt Nam rồi mới lấy ngày
        local_date = timezone.localtime(log.created_at).date()
        date_str = local_date.strftime('%d/%m')
        data_map[date_str] += 1

    # Tạo list dữ liệu cho biểu đồ (đảm bảo đủ 7 ngày liên tiếp)
    chart_dates = []
    chart_counts = []

    for i in range(6, -1, -1):
        d = timezone.now() - timedelta(days=i)
        d_str = d.strftime('%d/%m')  # Ví dụ: 20/12

        chart_dates.append(d_str)
        chart_counts.append(data_map.get(d_str, 0))

    # 3. Thống kê Top thiết bị (User-Agent) đăng nhập nhiều nhất

    ua_list = SecurityLog.objects.filter(event_type='LOGIN_SUCCESS').values_list('user_agent', flat=True)

    device_counter = Counter()

    for ua in ua_list:
        clean_name = _simplify_user_agent(ua)

        # Bỏ qua các log không xác định để bảng đẹp hơn
        if clean_name == "Không xác định":
            continue

        device_counter[clean_name] += 1

    # Lấy Top 5 thiết bị
    top_devices = []
    for name, count in device_counter.most_common(5):
        top_devices.append({
            'user_agent': name,
            'count': count
        })

    context = {
        "total_users": total_users,
        "users_2fa_on": users_2fa_on,
        "users_2fa_off": users_2fa_off,
        "total_otp_fails": total_otp_fails,
        "otp_locked_count": otp_locked_count,
        "chart_dates": chart_dates,
        "chart_counts": chart_counts,
        "top_devices": top_devices,
    }
    return render(request, "accounts/security_dashboard.html", context)

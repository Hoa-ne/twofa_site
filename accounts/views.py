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
from django.core.paginator import Paginator
from collections import defaultdict, Counter
from django.db.models import Count, F
from django.db.models.functions import TruncDate
from django.contrib.sessions.models import Session
import time
import secrets
import hmac

from django_ratelimit.decorators import ratelimit

from .models import User, SecurityPolicy, SecurityLog, SecurityConfig, BackupCode
from .forms import (
    RegisterForm, LoginForm, OTPForm, Enable2FAConfirmForm,
    ChangePasswordForm, BackupCodeForm, Disable2FAForm,
    ProfileEditForm, EmailConfirmationForm
)
from .tokens import email_verification_token
from .otp_algo import (
    generate_base32_secret, provisioning_uri, verify_totp,
    qr_code_base64
)

# Lay dia chi IP thuc cua client ke ca qua Proxy
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# Ham boc su dung IP lam key cho ratelimit
def ip_key_wrapper(group, request):
    return get_client_ip(request)

# Tao key gioi han tan suat dua tren IP va ten dang nhap
def get_ratelimit_key(group, request):
    ip = get_client_ip(request)
    username = ""

    if request.user.is_authenticated:
        username = request.user.username

    elif "pre_2fa_user_id" in request.session:
        try:
            uid = request.session["pre_2fa_user_id"]
            user = User.objects.get(pk=uid)
            username = user.username
        except User.DoesNotExist:
            username = "unknown"

    elif request.method == "POST" and "username" in request.POST:
        username = request.POST.get("username", "").strip()

    if not username:
        return ip

    return f"{ip}-{username}"

# Ghi lai nhat ky su kien bao mat vao he thong
def record_security_event(user, event_type, request=None, note=""):
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

# Thiet lap thoi gian het han cua phien dang nhap
def _set_session_expiry(request, remember_me: bool):
    if remember_me:
        expiry_seconds = getattr(settings, "SESSION_COOKIE_AGE", 2592000)
        request.session.set_expiry(expiry_seconds)
    else:
        request.session.set_expiry(0)

# Thuc hien dang nhap hoan chinh sau khi qua cac buoc kiem tra
def _perform_login(request, user, remember_me: bool):
    _set_session_expiry(request, remember_me)

    if remember_me:
        request.session['2fa_trusted'] = True
        request.session['2fa_trusted_user_id'] = user.id
    else:
        request.session.pop('2fa_trusted', None)
        request.session.pop('2fa_trusted_user_id', None)

    login(request, user)
    request.session.pop("pre_2fa_user_id", None)

    if user.must_setup_2fa and not user.is_2fa_enabled:
        return redirect("accounts:enable_2fa")
    if user.must_change_password:
        return redirect("accounts:change_password")
    return redirect("accounts:dashboard")

# Gui email kich hoat tai khoan cho nguoi dung moi
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

# Xu ly lien ket kich hoat tai khoan tu email
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

# Dang ky tai khoan moi va gui email kich hoat
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email_verified = False
            user.role = "USER"
            user.is_active = False

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

# Xu ly dang nhap kiem tra 2FA va phan quyen
@ratelimit(key=get_ratelimit_key, rate='10/m', block=True)
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            
            config = SecurityConfig.get_solo()

            must_have_2fa = False

            if user.role == 'ADMIN' or user.is_superuser:
                if config.enforce_for_admin:
                    must_have_2fa = True
            
            elif user.role == 'STAFF':
                if config.enforce_for_staff:
                    must_have_2fa = True
            
            else:
                if config.enforce_for_user:
                    must_have_2fa = True

            if user.must_setup_2fa:
                must_have_2fa = True

            if must_have_2fa:
                if not user.is_2fa_enabled:
                    login(request, user)
                    request.session.pop("pre_2fa_user_id", None)
                    
                    role_name = "Người dùng"
                    if user.role == 'ADMIN': role_name = "Quản trị viên"
                    elif user.role == 'STAFF': role_name = "Nhân viên"

                    messages.warning(
                        request,
                        f"Hệ thống yêu cầu nhóm {role_name} BẮT BUỘC bảo mật 2 lớp. Vui lòng kích hoạt ngay."
                    )
                    request.session.pop('2fa_trusted', None)
                    request.session.pop('2fa_trusted_user_id', None)
                    return redirect("accounts:enable_2fa")

                if request.session.get('2fa_trusted', False) and \
                   request.session.get('2fa_trusted_user_id') == user.id:
                    
                    record_security_event(user, "LOGIN_SUCCESS", request=request, note="Đăng nhập (Thiết bị tin cậy)")
                    return _perform_login(request, user, True)

                request.session["pre_2fa_user_id"] = user.id
                return redirect("accounts:otp_verify")

            if user.is_2fa_enabled:
                if request.session.get('2fa_trusted', False) and \
                   request.session.get('2fa_trusted_user_id') == user.id:
                    record_security_event(user, "LOGIN_SUCCESS", request=request, note="Đăng nhập (Thiết bị tin cậy)")
                    return _perform_login(request, user, True)

                request.session["pre_2fa_user_id"] = user.id
                return redirect("accounts:otp_verify")

            remember_me = False
            record_security_event(user, "LOGIN_SUCCESS", request=request, note="Đăng nhập không dùng 2FA")
            return _perform_login(request, user, remember_me)
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})

# Xac thuc ma OTP TOTP hoac Email de hoan tat dang nhap
@ratelimit(key=get_ratelimit_key, rate='10/m', block=True)
def otp_verify_view(request):
    user_id = request.session.get("pre_2fa_user_id")
    if not user_id:
        return redirect("accounts:login")

    user = get_object_or_404(User, pk=user_id)
    config = SecurityConfig.get_solo()

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

            if user.otp_secret:
                totp_ok = verify_totp(
                    user.otp_secret,
                    code,
                    period=config.otp_period,
                    digits=config.otp_digits,
                    algo="SHA1",
                    window=1
                )

            email_otp_code = request.session.get('email_otp_code')
            email_otp_expiry = request.session.get('email_otp_expiry', 0)

            if email_otp_code and hmac.compare_digest(code, email_otp_code) and time.time() < email_otp_expiry:
                email_ok = True
                request.session.pop('email_otp_code', None)
                request.session.pop('email_otp_expiry', None)

            if totp_ok or email_ok:
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
                user.failed_otp_attempts += 1
                note_msg = f"Nhập sai OTP lần thứ {user.failed_otp_attempts}"

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

# Gui ma OTP qua email cho nguoi dung
@ratelimit(key=ip_key_wrapper, rate='2/m', block=True)
def send_email_otp_view(request):
    user_id = request.session.get("pre_2fa_user_id")
    if not user_id:
        return redirect("accounts:login")

    user = get_object_or_404(User, pk=user_id)
    config = SecurityConfig.get_solo()

    if not config.allow_email_otp_system:
        messages.error(request, "Tính năng OTP qua Email đang bị TẮT trên toàn hệ thống.")
        return redirect("accounts:otp_verify")

    if not user.allow_email_otp:
        messages.error(request, "Tài khoản của bạn không được phép nhận mã qua Email.")
        return redirect("accounts:otp_verify")

    if request.method == "POST":
        form = EmailConfirmationForm(request.POST, user_email=user.email)
        
        if form.is_valid():
            last_sent = request.session.get('last_email_otp_sent', 0)
            if time.time() - last_sent < 60:
                messages.warning(request, "Vui lòng đợi 60 giây trước khi gửi lại mã.")
                return redirect("accounts:otp_verify")

            code = str(secrets.randbelow(900000) + 100000)
            request.session['email_otp_code'] = code
            request.session['email_otp_expiry'] = int(time.time()) + 300
            request.session['last_email_otp_sent'] = int(time.time())

            try:
                subject = f"Mã xác thực 2FA - {getattr(settings, 'SITE_NAME', 'TwoFA Demo')}"
                message = f"Mã xác thực 2FA của bạn là: {code}\n\nMã này có hiệu lực trong 5 phút."
                
                send_mail(
                    subject,
                    message,
                    getattr(settings, "DEFAULT_FROM_EMAIL", None),
                    [user.email],
                    fail_silently=False
                )

                record_security_event(user, "EMAIL_OTP_SENT", request=request, note="Đã xác thực email chính chủ trước khi gửi")
                messages.success(request, f"Đã gửi mã OTP đến email {user.email}.")
                
                return redirect("accounts:otp_verify")
                
            except Exception as e:
                messages.error(request, f"Lỗi khi gửi email: {e}")
                return redirect("accounts:otp_verify")
    else:
        form = EmailConfirmationForm()

    return render(request, "accounts/verify_email_otp.html", {
        "form": form,
        "username": user.username
    })

# Xac thuc bang ma du phong khi mat thiet bi OTP
@ratelimit(key=get_ratelimit_key, rate='10/m', block=True)
def backup_code_verify_view(request):
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

# Bat tinh nang xac thuc 2 lop va hien thi ma QR
@login_required
def enable_2fa_view(request):
    user = request.user
    config = SecurityConfig.get_solo()
    if not user.otp_secret:
        user.otp_secret = generate_base32_secret()
        user.save()

    otp_uri = provisioning_uri(
        account_name=user.username,
        issuer_name=getattr(settings, "SITE_NAME", "TwoFA Demo"),
        secret_b32=user.otp_secret,
        algo="SHA1",
        digits=config.otp_digits,
        period=config.otp_period,
    )
    qr_b64 = qr_code_base64(otp_uri)

    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["otp_code"]
            ok = verify_totp(
                user.otp_secret,
                code,
                digits=config.otp_digits,
                period=config.otp_period,
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

# Hien thi danh sach ma du phong sau khi bat 2FA
@login_required
def enable_2fa_complete_view(request):
    backup_codes = request.session.pop('backup_codes', None)
    if not backup_codes:
        return redirect("accounts:dashboard")

    return render(
        request,
        "accounts/enable_2fa_complete.html",
        {"backup_codes": backup_codes}
    )

# Cho phep nguoi dung tu doi mat khau
@login_required
@ratelimit(key=get_ratelimit_key, rate='10/m', block=True)
def change_password_view(request):
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

            login(request, user)
            return redirect("accounts:dashboard")
    else:
        form = ChangePasswordForm(user)
    return render(request, "accounts/change_password.html", {"form": form})

# Trang tong quan tai khoan va trang thai bao mat
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

# Dang xuat va xoa trang thai thiet bi tin cay
def logout_view(request):
    request.session.pop('2fa_trusted', None)
    request.session.pop('2fa_trusted_user_id', None)
    logout(request)
    return redirect("forum:home")

# Trang danh rieng cho nhan vien noi bo
@login_required
def staff_only_view(request):
    if not request.user.is_staff_role():
        return HttpResponseForbidden("Bạn không có quyền STAFF.")
    return render(request, "accounts/dashboard.html", {"staff": True})

# Chinh sua thong tin ho so ca nhan
@login_required
def profile_edit_view(request):
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật hồ sơ thành công!")
            return redirect("accounts:profile_view", pk=request.user.pk)
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, "accounts/profile_edit.html", {"form": form})

# Xem chi tiet ho so va bai viet cua nguoi dung
def profile_view(request, pk):
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

# Tat tinh nang xac thuc 2 lop bang ma du phong
@login_required
def disable_2fa_view(request):
    user = request.user
    if not user.is_2fa_enabled:
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = Disable2FAForm(user, request.POST)
        if form.is_valid():
            code_input = form.cleaned_data["backup_code"]
            
            if user.verify_backup_code(code_input):
                user.is_2fa_enabled = False
                user.otp_secret = None
                user.must_setup_2fa = False
                user.save()
                
                BackupCode.objects.filter(user=user).delete()

                messages.success(request, "Đã tắt xác thực 2 lớp thành công.")
                request.session.pop('2fa_trusted', None)
                return redirect("accounts:dashboard")
            else:
                form.add_error("backup_code", "Mã dự phòng không đúng hoặc đã được sử dụng.")
    else:
        form = Disable2FAForm(user)

    return render(request, "accounts/disable_2fa.html", {"form": form})

# Trang thong bao loi khi vuot qua gioi han truy cap
def ratelimited_error_view(request, exception=None):
    return render(request, 'ratelimited.html', status=403)

# Rut gon chuoi User-Agent thanh ten trinh duyet de doc
def _simplify_user_agent(ua_string):
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

# Trang tong quan bao mat danh cho quan tri vien
@login_required
def security_dashboard_view(request):
    if not request.user.is_staff_role():
        return HttpResponseForbidden("Bạn không có quyền truy cập.")

    total_users = User.objects.count()
    users_2fa_on = User.objects.filter(is_2fa_enabled=True).count()
    users_2fa_off = total_users - users_2fa_on
    otp_locked_count = User.objects.filter(otp_locked=True).count()
    total_otp_fails = SecurityLog.objects.filter(event_type='OTP_FAIL').count()

    last_7_days = timezone.now() - timedelta(days=7)

    logs = SecurityLog.objects.filter(event_type='OTP_FAIL', created_at__gte=last_7_days)

    data_map = defaultdict(int)

    for log in logs:
        local_date = timezone.localtime(log.created_at).date()
        date_str = local_date.strftime('%d/%m')
        data_map[date_str] += 1

    chart_dates = []
    chart_counts = []

    for i in range(6, -1, -1):
        d = timezone.now() - timedelta(days=i)
        d_str = d.strftime('%d/%m')

        chart_dates.append(d_str)
        chart_counts.append(data_map.get(d_str, 0))

    ua_list = SecurityLog.objects.filter(event_type='LOGIN_SUCCESS').values_list('user_agent', flat=True)

    device_counter = Counter()

    for ua in ua_list:
        clean_name = _simplify_user_agent(ua)

        if clean_name == "Không xác định":
            continue

        device_counter[clean_name] += 1

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

# Xoa tat ca phien dang nhap cua nguoi dung khoi database
def logout_all_devices_logic(user):
    all_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    
    deleted_count = 0
    for session in all_sessions:
        data = session.get_decoded()
        if str(user.id) == str(data.get('_auth_user_id')):
            session.delete()
            deleted_count += 1
    return deleted_count

# Xu ly dang xuat khoi tat ca thiet bi
@login_required
def logout_all_view(request):
    count = logout_all_devices_logic(request.user)
    
    logout(request)
    
    messages.success(request, f"Đã đăng xuất thành công khỏi {count} thiết bị/phiên đăng nhập!")
    return redirect("accounts:login")
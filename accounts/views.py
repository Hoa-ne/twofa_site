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

from django.db.models import Count
from datetime import timedelta
# MỚI: Import decorator của ratelimit
from django_ratelimit.decorators import ratelimit

from .models import User, SecurityPolicy, SecurityLog, SecurityConfig
# Sửa import: Thêm BackupCodeForm VÀ Disable2FAForm
from .forms import (
    RegisterForm, LoginForm, OTPForm, Enable2FAConfirmForm, 
    ChangePasswordForm, BackupCodeForm, Disable2FAForm
)
from .tokens import email_verification_token
# Sửa import: Bỏ qr_code_base64 từ utils
from .otp_algo import (
    generate_base32_secret, provisioning_uri, verify_totp,
    qr_code_base64 # Lấy qr_code_base64 từ đây
)
from django.db.models import Count, F
from django.db.models.functions import TruncDate
# Thêm các import cần thiết
import time
import secrets
import hmac

# SỬA: Đổi tên hàm _log_event -> record_security_event
def record_security_event(user, event_type, request=None, note=""):
    """
    Hàm trợ giúp mới để ghi lại nhật ký sự kiện bảo mật.
    """
    # SỬA: Gọi hàm get_client_ip thay vì lấy trực tiếp REMOTE_ADDR
    user_ip = get_client_ip(request) if request else ""
    
    # Lấy User-Agent (Thiết bị/Trình duyệt) để lưu vào nếu bạn đã thêm trường này
    ua_string = ""
    if request:
        ua_string = request.META.get('HTTP_USER_AGENT', "")[:255]

    SecurityLog.objects.create(
        user=user,
        event_type=event_type,
        ip=user_ip,  # <--- Đã dùng IP chuẩn
        # user_agent=ua_string, # Bỏ comment dòng này nếu bạn đã thêm cột user_agent vào model ở bước trước
        note=note,
        created_at=timezone.now(),
    )

# --- (SỬA LẠI HOÀN TOÀN) Hàm trợ giúp cho session -----------------
def _set_session_expiry(request, remember_me: bool):
    """(SỬA LẠI) Đặt thời hạn session: 0 (đóng browser) hoặc 30 ngày."""
    if remember_me:
        # Lấy từ settings, nếu không có thì 30 ngày
        expiry_seconds = getattr(settings, "SESSION_COOKIE_AGE", 2592000)
        request.session.set_expiry(expiry_seconds)
    else:
        request.session.set_expiry(0) # Hết hạn khi đóng browser

def _perform_login(request, user, remember_me: bool):
    """
    (SỬA LẠI) Hàm trợ giúp: Đặt session expiry, cờ trusted-device VÀ login user.
    """
    # 1. Đặt thời gian hết hạn
    _set_session_expiry(request, remember_me)
    
    # 2. Đặt cờ tin cậy (trusted flag) gắn liền với user ID
    if remember_me:
        request.session['2fa_trusted'] = True
        request.session['2fa_trusted_user_id'] = user.id
    else:
        # Xóa cờ nếu không "Nhớ"
        request.session.pop('2fa_trusted', None)
        request.session.pop('2fa_trusted_user_id', None)

    # 3. Login và dọn dẹp
    login(request, user)
    request.session.pop("pre_2fa_user_id", None)
    
    # 4. Chuyển hướng
    if user.must_setup_2fa and not user.is_2fa_enabled:
        return redirect("accounts:enable_2fa")
    if user.must_change_password:
        return redirect("accounts:change_password")
    return redirect("accounts:dashboard")
# -----------------------------------------------


def send_activation_email(request, user):
    # ... (giữ nguyên hàm send_activation_email) ...
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
    # ... (giữ nguyên hàm activate_email_view) ...
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
    # ... (giữ nguyên hàm register_view) ...
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


# MỚI: Thêm decorator @ratelimit (5 lần/phút/IP)
@ratelimit(key='ip', rate='5/m', block=True)
def login_view(request):
    """
    (SỬA LẠI) Bước 1: đăng nhập bằng mật khẩu.
    - Sửa đổi: Vá lỗ hổng '2fa_trusted' global.
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]

            policy = SecurityPolicy.objects.first()
            config = SecurityConfig.get_solo() 

            enforce_all = bool(getattr(policy, "require_2fa_for_new_users", True)) # Logic cũ
            if user.is_staff or user.is_superuser:
                enforce_all = True
            
            # --- LOGIC KIỂM TRA BẮT BUỘC 2FA TOÀN TRANG ---
            if config.enforce_2fa:
                if not user.is_2fa_enabled:
                    login(request, user) 
                    request.session.pop("pre_2fa_user_id", None)
                    messages.warning(request, "Hệ thống đang yêu cầu BẮT BUỘC 2FA. Vui lòng kích hoạt 2FA.")
                    # Xóa cờ tin cậy (nếu có) phòng trường hợp user cũ
                    request.session.pop('2fa_trusted', None)
                    request.session.pop('2fa_trusted_user_id', None)
                    return redirect("accounts:enable_2fa")
                
                # --- (SỬA LẠI LOGIC NÀY) ---
                # User đã bật 2FA, kiểm tra xem thiết bị có được tin cậy KHÔNG
                if request.session.get('2fa_trusted', False) and \
                   request.session.get('2fa_trusted_user_id') == user.id:
                    
                    # User này đã được tin cậy trên trình duyệt này -> bỏ qua OTP
                    record_security_event(user, "LOGIN_SUCCESS", request=request, note="Login success (Trusted Device, User Matched)")
                    return _perform_login(request, user, True) # Giữ nguyên tin cậy
                
                # Nếu không tin cậy -> Đi tới trang OTP
                request.session["pre_2fa_user_id"] = user.id
                return redirect("accounts:otp_verify")
            
            # --- LOGIC CŨ (Nếu config.enforce_2fa = False) ---
            if user.is_2fa_enabled:
                
                # --- (SỬA LẠI LOGIC NÀY) ---
                if request.session.get('2fa_trusted', False) and \
                   request.session.get('2fa_trusted_user_id') == user.id:
                    
                    record_security_event(user, "LOGIN_SUCCESS", request=request, note="Login success (Trusted Device, User Matched)")
                    return _perform_login(request, user, True) # Giữ nguyên tin cậy

                request.session["pre_2fa_user_id"] = user.id
                return redirect("accounts:otp_verify")

            # --- Login không 2FA ---
            remember_me = False 
            record_security_event(user, "LOGIN_SUCCESS", request=request, note="Login without 2FA yet")
            return _perform_login(request, user, remember_me)
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


@ratelimit(key='ip', rate='5/m', block=True)
def otp_verify_view(request):
    # ... (giữ nguyên hàm otp_verify_view) ...
    user_id = request.session.get("pre_2fa_user_id")
    if not user_id:
        return redirect("accounts:login")

    user = get_object_or_404(User, pk=user_id)
    config = SecurityConfig.get_solo()
    
    if user.otp_locked:
        record_security_event(user, "OTP_LOCKED", request=request, note="User tried while locked")
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
                totp_ok = verify_totp(user.otp_secret, code, period=30, digits=6, algo="SHA1", window=1)

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

                note = "OTP (TOTP) ok" if totp_ok else "OTP (Email) ok"
                record_security_event(user, "OTP_SUCCESS", request=request, note=f"{note}, full login")

                return _perform_login(request, user, remember_me)
            else:
                user.failed_otp_attempts += 1
                note_msg = f"OTP failed attempt {user.failed_otp_attempts}"
                
                if user.failed_otp_attempts >= config.lockout_threshold: 
                    user.otp_locked = True
                    note_msg += " -> LOCKED"
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

@ratelimit(key='ip', rate='2/m', block=True)
def send_email_otp_view(request):
    # ... (giữ nguyên hàm send_email_otp_view) ...
    user_id = request.session.get("pre_2fa_user_id")
    if not user_id:
        return redirect("accounts:login")
    
    user = get_object_or_404(User, pk=user_id)

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
        message = (
            f"Mã xác thực 2FA của bạn là: {code}\n\n"
            f"Mã này có hiệu lực trong 5 phút.\n"
        )
        send_mail(subject, message, getattr(settings, "DEFAULT_FROM_EMAIL", None), [user.email], fail_silently=False)
        
        record_security_event(user, "EMAIL_OTP_SENT", request=request)
        messages.success(request, f"Đã gửi mã OTP đến email {user.email}.")
    except Exception as e:
        messages.error(request, f"Lỗi khi gửi email: {e}")

    return redirect("accounts:otp_verify")

@ratelimit(key='ip', rate='5/m', block=True)
def backup_code_verify_view(request):
    # ... (giữ nguyên hàm backup_code_verify_view) ...
    user_id = request.session.get("pre_2fa_user_id")
    if not user_id:
        return redirect("accounts:login")

    user = get_object_or_404(User, pk=user_id)
    config = SecurityConfig.get_solo()

    if user.otp_locked:
        return render(
            request, "accounts/backup_code_verify.html",
            {
                "form": BackupCodeForm(), "username": user.username, "locked": True,
                "error": f"Tài khoản đã bị khóa OTP do nhập sai quá {config.lockout_threshold} lần. Liên hệ admin."
            }, status=403,
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
                
                record_security_event(user, "BACKUP_CODE_USED", request=request, note="Login success (Backup Code)")

                return _perform_login(request, user, remember_me)
            else:
                user.failed_otp_attempts += 1
                note_msg = f"Backup code failed attempt {user.failed_otp_attempts}"
                
                if user.failed_otp_attempts >= config.lockout_threshold:
                    user.otp_locked = True
                    note_msg += " -> LOCKED"
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
    # ... (giữ nguyên hàm enable_2fa_view) ...
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
                
                record_security_event(user, "ENABLE_2FA", request=request, note="User enabled 2FA (TOTP)")

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
    # ... (giữ nguyên hàm enable_2fa_complete_view) ...
    backup_codes = request.session.pop('backup_codes', None)
    if not backup_codes:
        return redirect("accounts:dashboard")
    
    return render(
        request, 
        "accounts/enable_2fa_complete.html",
        {"backup_codes": backup_codes}
    )

@login_required
@ratelimit(key='ip', rate='5/m', block=True)
def change_password_view(request):
    # ... (giữ nguyên hàm change_password_view) ...
    user = request.user
    if request.method == "POST":
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            new_pw = form.cleaned_data["new_password1"]
            user.set_password(new_pw)
            user.must_change_password = False
            user.save()

            record_security_event(user, "PASSWORD_CHANGED", request=request, note="User changed their own password")
            
            login(request, user) 
            return redirect("accounts:dashboard")
    else:
        form = ChangePasswordForm(user)
    return render(request, "accounts/change_password.html", {"form": form})


@login_required
def dashboard_view(request):
    # ... (giữ nguyên hàm dashboard_view) ...
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
    # --- (SỬA LẠI HÀM NÀY) ---
    # Xóa cả 2 cờ session khi logout
    request.session.pop('2fa_trusted', None)
    request.session.pop('2fa_trusted_user_id', None)
    logout(request)
    return redirect("forum:home")


@login_required
def staff_only_view(request):
    # ... (giữ nguyên hàm staff_only_view) ...
    if not request.user.is_staff_role():
        return HttpResponseForbidden("Bạn không có quyền STAFF.")
    return render(request, "accounts/dashboard.html", {"staff": True})

@login_required
def profile_edit_view(request):
    # ... (giữ nguyên hàm profile_edit_view) ...
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật hồ sơ thành công!")
            return redirect("accounts:profile_view", username=request.user.username)
    else:
        form = ProfileEditForm(instance=request.user)
    
    return render(request, "accounts/profile_edit.html", {"form": form})

def profile_view(request, username):
    # ... (giữ nguyên hàm profile_view) ...
    profile_user = get_object_or_404(User, username=username)
    
    post_list = profile_user.post_set.all().order_by("-created_at")
    paginator = Paginator(post_list, 10) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        "profile_user": profile_user,
        "page_obj": page_obj
    }
    return render(request, "accounts/profile_view.html", context)

@login_required
@ratelimit(key='ip', rate='5/m', block=True)
def disable_2fa_view(request):
    # ... (giữ nguyên hàm disable_2fa_view) ...
    user = request.user
    if not user.is_2fa_enabled:
        messages.error(request, "2FA chưa được bật.")
        return redirect("accounts:dashboard")
    
    if request.method == "POST":
        form = Disable2FAForm(user, request.POST)
        if form.is_valid():
            code = form.cleaned_data["otp_code"]
            ok = verify_totp(user.otp_secret, code, period=30, digits=6, algo="SHA1", window=1)

            if ok:
                user.is_2fa_enabled = False
                user.otp_secret = None
                user.failed_otp_attempts = 0
                user.otp_locked = False
                user.save()
                
                user.backup_codes.all().delete()
                
                record_security_event(user, "DISABLE_2FA", request=request, note="User disabled 2FA (self)")
                messages.success(request, "Xác thực hai lớp (2FA) đã được tắt.")
                return redirect("accounts:dashboard")
            else:
                form.add_error("otp_code", "Mã OTP không hợp lệ.")
    else:
        form = Disable2FAForm(user)
        
    return render(request, "accounts/disable_2fa.html", {"form": form})
    
@login_required
def security_dashboard_view(request):
    if not request.user.is_staff_role():
        return HttpResponseForbidden("Bạn không có quyền truy cập.")

    # 1. Thống kê User
    total_users = User.objects.count()
    users_2fa_on = User.objects.filter(is_2fa_enabled=True).count()
    users_2fa_off = total_users - users_2fa_on
    otp_locked_count = User.objects.filter(otp_locked=True).count()

    # 2. Thống kê OTP Fail tổng cộng
    total_otp_fails = SecurityLog.objects.filter(event_type='OTP_FAIL').count()

    # 3. Dữ liệu biểu đồ: Số lần sai OTP trong 7 ngày qua
    last_7_days = timezone.now() - timedelta(days=7)
    
    # Group by Date (Ngày): Đếm số lỗi theo từng ngày
    fails_by_date = (
        SecurityLog.objects
        .filter(event_type='OTP_FAIL', created_at__gte=last_7_days)
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )
    
    # Chuyển dữ liệu thành list để vẽ biểu đồ
    chart_dates = [item['date'].strftime('%d/%m') for item in fails_by_date]
    chart_counts = [item['count'] for item in fails_by_date]

    # 4. Thống kê Thiết bị (User Agent) - Lấy Top 5 thiết bị đăng nhập nhiều nhất
    top_devices = (
        SecurityLog.objects
        .filter(event_type='LOGIN_SUCCESS')
        .values('user_agent')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )

    context = {
        "total_users": total_users,
        "users_2fa_on": users_2fa_on,
        "users_2fa_off": users_2fa_off,
        "total_otp_fails": total_otp_fails,
        "otp_locked_count": otp_locked_count,
        
        # Dữ liệu cho biểu đồ
        "chart_dates": chart_dates,
        "chart_counts": chart_counts,
        
        # Dữ liệu thiết bị
        "top_devices": top_devices,
    }
    return render(request, "accounts/security_dashboard.html", context)
    
# --- THÊM HÀM MỚI NÀY ĐỂ LẤY IP THẬT ---
def get_client_ip(request):
    """
    Lấy IP thật của người dùng, ưu tiên header X-Forwarded-For
    (Dùng khi chạy sau Proxy hoặc Nginx/Cloudflare)
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # Header này có thể chứa danh sách IP: "client, proxy1, proxy2"
        # Ta lấy cái đầu tiên là IP client thật
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        # Fallback về REMOTE_ADDR nếu không có proxy
        ip = request.META.get('REMOTE_ADDR')
    return ip

def ratelimited_error_view(request, exception=None):
    # ... (giữ nguyên hàm ratelimited_error_view) ...
    return render(request, 'ratelimited.html', status=403)
    
# --- HÀM PHỤ ĐỂ DỊCH USER-AGENT CHO GỌN ---
def _simplify_user_agent(ua_string):
    if not ua_string or ua_string == "Unknown":
        return "Không xác định"
    
    ua = ua_string.lower()
    
    # 1. Xác định Hệ điều hành (OS)
    os = "Khác"
    if "windows" in ua: os = "Windows"
    elif "mac os" in ua: os = "macOS"
    elif "android" in ua: os = "Android"
    elif "iphone" in ua or "ipad" in ua: os = "iOS"
    elif "linux" in ua: os = "Linux"

    # 2. Xác định Trình duyệt
    browser = "Browser"
    if "edg" in ua: browser = "Edge" # Edge thường chứa cả Chrome nên check trước
    elif "chrome" in ua: browser = "Chrome"
    elif "firefox" in ua: browser = "Firefox"
    elif "safari" in ua: browser = "Safari"
    elif "opera" in ua or "opr" in ua: browser = "Opera"
    
    return f"{os} ({browser})"

# --- HÀM VIEW CHÍNH ĐÃ SỬA ---
@login_required
def security_dashboard_view(request):
    if not request.user.is_staff_role():
        return HttpResponseForbidden("Bạn không có quyền truy cập.")

    # 1. Thống kê User
    total_users = User.objects.count()
    users_2fa_on = User.objects.filter(is_2fa_enabled=True).count()
    users_2fa_off = total_users - users_2fa_on
    otp_locked_count = User.objects.filter(otp_locked=True).count()

    # 2. Thống kê OTP Fail tổng cộng
    total_otp_fails = SecurityLog.objects.filter(event_type='OTP_FAIL').count()

    # 3. Dữ liệu biểu đồ: Số lần sai OTP trong 7 ngày qua
    last_7_days = timezone.now() - timedelta(days=7)
    
    fails_by_date = (
        SecurityLog.objects
        .filter(event_type='OTP_FAIL', created_at__gte=last_7_days)
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )
    
    chart_dates = [item['date'].strftime('%d/%m') for item in fails_by_date]
    chart_counts = [item['count'] for item in fails_by_date]

    # 4. Thống kê Thiết bị (Đã xử lý chuỗi User-Agent cho gọn)
    raw_devices = (
        SecurityLog.objects
        .filter(event_type='LOGIN_SUCCESS')
        .values('user_agent')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )

    # Xử lý danh sách: Dịch User-Agent sang tên ngắn gọn
    top_devices = []
    for item in raw_devices:
        clean_name = _simplify_user_agent(item['user_agent'])
        top_devices.append({
            'user_agent': clean_name, # Tên mới gọn gàng
            'count': item['count']
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
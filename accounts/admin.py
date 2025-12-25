from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils import timezone
from django.utils.html import format_html

from .models import User, SecurityPolicy, SecurityLog, BackupCode, SecurityConfig
from .otp_algo import generate_base32_secret as create_otp_secret
from .forms import UserAdminCreationForm, UserAdminChangeForm


# Ham ghi lai nhat ky hoat dong cua admin vao he thong
def log_admin_action(request, user, event_type, note=""):
    SecurityLog.objects.create(
        user=user,
        event_type=event_type, 
        ip=request.META.get("REMOTE_ADDR", ""),
        note=note,
        created_at=timezone.now(),
    )

@admin.action(description="Cho phép nhận OTP qua mail")
# Ham cho phep nguoi dung nhan ma OTP qua email hang loat
def enable_email_otp(modeladmin, request, queryset):
    updated = queryset.update(allow_email_otp=True)
    messages.success(request, f"Đã cho phép {updated} người dùng sử dụng OTP Email.")

@admin.action(description="Chặn nhận OTP qua mail - Bắt dùng App")
# Ham chan nguoi dung nhan ma OTP qua email hang loat
def disable_email_otp(modeladmin, request, queryset):
    updated = queryset.update(allow_email_otp=False)
    messages.success(request, f"Đã chặn OTP Email của {updated} người dùng.")

@admin.action(description="Reset mã OTP & Yêu cầu cài đặt lại")
# Ham reset ma bi mat OTP va yeu cau nguoi dung cai dat lai tu dau
def reset_otp_secret(modeladmin, request, queryset):
    count = 0
    for user in queryset:
        user.otp_secret = create_otp_secret()
        user.is_2fa_enabled = False
        user.must_setup_2fa = True
        user.failed_otp_attempts = 0
        user.otp_locked = False
        user.must_change_password = True
        user.save()
        BackupCode.objects.filter(user=user).delete() 
        log_admin_action(request, user, "RESET_OTP", note="Admin reset OTP secret + force pw reset")
        count += 1
    messages.success(request, f"Đã reset OTP cho {count} người dùng. Họ sẽ phải quét mã QR mới.")

@admin.action(description="Bật yêu cầu thiết lập 2FA")
# Ham bat buoc nguoi dung phai thiet lap xac thuc 2 lop
def force_require_2fa(modeladmin, request, queryset):
    updated = queryset.update(must_setup_2fa=True)
    for u in queryset:
        log_admin_action(request, u, "FORCED_2FA", note="must_setup_2fa=True")
    messages.success(request, f"Đã bật yêu cầu ép buộc 2FA cho {updated} người dùng.")

@admin.action(description="Tắt yêu cầu thiết lập 2FA")
# Ham huy bo yeu cau bat buoc thiet lap xac thuc 2 lop
def disable_require_2fa(modeladmin, request, queryset):
    updated = queryset.update(must_setup_2fa=False)
    messages.success(request, f"Đã tắt yêu cầu ép buộc 2FA cho {updated} người dùng.")

@admin.action(description="Tắt xác thực 2 lớp (2FA) hiện tại")
# Ham tat tinh nang xac thuc 2 lop cho cac tai khoan duoc chon
def disable_2fa(modeladmin, request, queryset):
    updated_count = 0
    for user in queryset:
        if user.is_2fa_enabled:
            user.is_2fa_enabled = False
            user.save()
            log_admin_action(request, user, "DISABLE_2FA", note="Admin disabled 2FA")
            updated_count += 1
    messages.success(request, f"Đã tắt 2FA cho {updated_count} người dùng.")

@admin.action(description="Mở khóa OTP (do nhập sai nhiều lần)")
# Ham mo khoa tai khoan bi khoa do nhap sai OTP qua nhieu lan
def unlock_otp(modeladmin, request, queryset):
    updated = 0
    for user in queryset:
        user.otp_locked = False
        user.failed_otp_attempts = 0
        user.save()
        log_admin_action(request, user, "OTP_LOCKED", note="Admin unlocked OTP manually")
        updated += 1
    messages.success(request, f"Đã mở khóa OTP cho {updated} người dùng.")

@admin.action(description="Yêu cầu đổi mật khẩu lần sau")
# Ham yeu cau nguoi dung phai doi mat khau trong lan dang nhap tiep theo
def force_password_reset(modeladmin, request, queryset):
    updated = queryset.update(must_change_password=True)
    messages.success(request, f"Đã yêu cầu {updated} người dùng phải đổi mật khẩu.")

@admin.action(description="Hủy yêu cầu đổi mật khẩu")
# Ham huy bo yeu cau doi mat khau cho nguoi dung
def clear_password_reset_flag(modeladmin, request, queryset):
    updated = queryset.update(must_change_password=False)
    messages.success(request, f"Đã hủy yêu cầu đổi mật khẩu cho {updated} người dùng.")


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = (
        "get_username", "get_email", "get_role", "get_email_verified",
        "get_is_2fa_enabled", "allow_email_otp", "get_otp_locked", 
        "get_is_staff", "get_is_superuser"
    )

    list_filter = (
        "role", "email_verified", "is_2fa_enabled",
        "allow_email_otp", 
        "otp_locked", "is_staff", "is_superuser", "is_active",
    )

    search_fields = ("username", "email")
    ordering = ("username",)

    actions = [
        reset_otp_secret, force_require_2fa, disable_require_2fa,
        disable_2fa, unlock_otp, force_password_reset,
        clear_password_reset_flag,
        enable_email_otp, disable_email_otp 
    ]

    @admin.display(description="Tên đăng nhập", ordering="username")
    # Ham lay ten dang nhap cua nguoi dung
    def get_username(self, obj):
        return obj.username

    @admin.display(description="Email", ordering="email")
    # Ham lay dia chi email cua nguoi dung
    def get_email(self, obj):
        return obj.email

    @admin.display(description="Vai trò", ordering="role")
    # Ham lay vai tro cua nguoi dung trong he thong
    def get_role(self, obj):
        return obj.role

    @admin.display(description="Đã xác thực Email", ordering="email_verified", boolean=True)
    # Ham kiem tra xem email da duoc xac thuc chua
    def get_email_verified(self, obj):
        return obj.email_verified

    @admin.display(description="Đã bật 2FA", ordering="is_2fa_enabled", boolean=True)
    # Ham kiem tra xem nguoi dung da bat xac thuc 2 lop chua
    def get_is_2fa_enabled(self, obj):
        return obj.is_2fa_enabled

    @admin.display(description="Khóa OTP", ordering="otp_locked", boolean=True)
    # Ham kiem tra xem tai khoan co bi khoa OTP khong
    def get_otp_locked(self, obj):
        return obj.otp_locked

    @admin.display(description="Nhân viên", ordering="is_staff", boolean=True)
    # Ham kiem tra xem nguoi dung co phai la nhan vien khong
    def get_is_staff(self, obj):
        return obj.is_staff

    @admin.display(description="Siêu quản trị", ordering="is_superuser", boolean=True)
    # Ham kiem tra xem nguoi dung co phai la sieu quan tri khong
    def get_is_superuser(self, obj):
        return obj.is_superuser

    @admin.display(description="Mật khẩu")
    # Ham tao duong link dan den trang thay doi mat khau
    def link_doi_mat_khau(self, obj):
        if obj.pk:
            return format_html('<a class="button" href="../password/">Đổi mật khẩu</a>')
        return "-"

    readonly_fields = ('link_doi_mat_khau',)

    fieldsets = (
        (None, {"fields": ("username", "link_doi_mat_khau")}),
        ("Thông tin cá nhân", {"fields": ("first_name", "last_name", "nickname", "email", "avatar", "bio")}),
        ("Quyền hệ thống", {
            "fields": (
                "role", "is_active", "is_staff", "is_superuser", "groups", "user_permissions",
            )
        }),
        ("Bảo mật & 2FA", {
            "fields": (
                "email_verified",
                "is_2fa_enabled",
                "allow_email_otp",
                "must_setup_2fa",
                "failed_otp_attempts",
                "otp_locked",
                "must_change_password",
            )
        }),
        ("Thời gian", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "email", "password1", "password2",  
                "role", "is_staff", "is_superuser", "must_setup_2fa",
            ),
        }),
    )


@admin.register(SecurityPolicy)
class SecurityPolicyAdmin(admin.ModelAdmin):
    list_display = ("get_require_2fa", "get_updated_at")
    
    @admin.display(description="Yêu cầu 2FA cho người dùng mới", ordering="require_2fa_for_new_users", boolean=True)
    # Ham lay trang thai yeu cau 2FA doi voi nguoi dung moi dang ky
    def get_require_2fa(self, obj):
        return obj.require_2fa_for_new_users

    @admin.display(description="Cập nhật lần cuối", ordering="updated_at")
    # Ham lay thoi gian cap nhat lan cuoi cung
    def get_updated_at(self, obj):
        return obj.updated_at

    actions = ["force_all", "disable_all"]

    @admin.action(description="Ép TOÀN BỘ người dùng phải bật 2FA")
    # Ham ep buoc tat ca nguoi dung trong he thong phai su dung 2FA
    def force_all(self, request, queryset):
        updated = User.objects.update(must_setup_2fa=True)
        messages.success(request, f"Đã ép {updated} người dùng phải bật 2FA.")

    @admin.action(description="Bỏ ép buộc 2FA cho TOÀN BỘ người dùng")
    # Ham bo ep buoc su dung 2FA cho tat ca nguoi dung
    def disable_all(self, request, queryset):
        updated = User.objects.update(must_setup_2fa=False)
        messages.success(request, f"Đã bỏ ép buộc 2FA cho {updated} người dùng.")

@admin.register(SecurityLog)
class SecurityLogAdmin(admin.ModelAdmin):
    list_display = ("get_created_at", "get_user", "get_event", "get_ip", "get_note")
    list_filter = ("event_type", "user")
    search_fields = ("user__username", "ip", "note")
    ordering = ("-created_at",)
    readonly_fields = ("user", "event_type", "ip", "note", "created_at")


    @admin.display(description="Thời gian", ordering="created_at")
    # Ham lay thoi gian tao log bao mat
    def get_created_at(self, obj):
        return obj.created_at

    @admin.display(description="Người dùng", ordering="user")
    # Ham lay thong tin nguoi dung lien quan den log
    def get_user(self, obj):
        return obj.user

    @admin.display(description="Sự kiện", ordering="event_type")
    # Ham chuyen doi ma su kien sang tieng Viet de hien thi
    def get_event(self, obj):
        translate = {
            "OTP_SUCCESS": " OTP thành công",
            "OTP_FAIL": " Nhập sai OTP",
            "OTP_LOCKED": " Bị khóa OTP",
            "LOGIN_SUCCESS": "Đăng nhập thường",
            "ENABLE_2FA": "Bật 2FA",
            "DISABLE_2FA": "Tắt 2FA",
            "BACKUP_CODE_USED": "Dùng mã dự phòng",
            "EMAIL_OTP_SENT": "Đã gửi Email OTP",
            "RESET_OTP": "Admin Reset OTP",
            "FORCED_2FA": "Admin ép bật 2FA",
        }
        return translate.get(obj.event_type, obj.event_type)

    @admin.display(description="Địa chỉ IP", ordering="ip")
    # Ham lay dia chi IP thuc hien hanh dong
    def get_ip(self, obj):
        return obj.ip

    @admin.display(description="Ghi chú", ordering="note")
    # Ham lay noi dung ghi chu chi tiet cua log
    def get_note(self, obj):
        return obj.note

    # Ham chan khong cho phep them log thu cong
    def has_add_permission(self, request): return False
    # Ham chan khong cho phep sua doi log thu cong
    def has_change_permission(self, request, obj=None): return False

@admin.register(BackupCode)
class BackupCodeAdmin(admin.ModelAdmin):
    list_display = ("get_user", "get_is_used", "get_created_at")
    list_filter = ("is_used", "user")
    search_fields = ("user__username",)
    ordering = ("-created_at",)
    readonly_fields = ("user", "code_hash", "is_used", "created_at")

    @admin.display(description="Người dùng", ordering="user")
    # Ham lay thong tin nguoi dung so huu ma du phong
    def get_user(self, obj):
        return obj.user

    @admin.display(description="Đã sử dụng", ordering="is_used", boolean=True)
    # Ham kiem tra xem ma du phong da duoc su dung chua
    def get_is_used(self, obj):
        return obj.is_used

    @admin.display(description="Ngày tạo", ordering="created_at")
    # Ham lay thoi gian tao ma du phong
    def get_created_at(self, obj):
        return obj.created_at

    # Ham chan khong cho phep them ma du phong thu cong
    def has_add_permission(self, request): return False
    # Ham chan khong cho phep sua doi ma du phong thu cong
    def has_change_permission(self, request, obj=None): return False

@admin.register(SecurityConfig)
class SecurityConfigAdmin(admin.ModelAdmin):
    list_display = ("__str__", "otp_digits", "otp_period", "allow_email_otp_system")
    
    fieldsets = (
        ("Cấu hình OTP (Quan trọng)", {
            "fields": ("otp_digits", "otp_period", "lockout_threshold") 
        }),
        ("Phân quyền Bắt buộc 2FA", {
            "fields": ("enforce_for_admin", "enforce_for_staff", "enforce_for_user"),
            "description": "Tích chọn nhóm nào thì nhóm đó sẽ bị BẮT BUỘC phải bật 2FA khi đăng nhập."
        }),
        ("Cấu hình Email OTP", {
            "fields": ("allow_email_otp_system",),
            "description": "Nếu bỏ tích: Toàn bộ hệ thống sẽ KHÔNG được dùng Email để nhận OTP."
        }),
    )

    # Ham kiem tra quyen them moi chi cho phep ton tai mot cau hinh duy nhat
    def has_add_permission(self, request):
        if SecurityConfig.objects.exists():
            return False
        return True

    # Ham chan khong cho phep xoa cau hinh he thong
    def has_delete_permission(self, request, obj=None):
        return False
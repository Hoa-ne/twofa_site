from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User
from .utils import create_otp_secret
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, SecurityPolicy
from .utils import create_otp_secret


@admin.action(description="Reset OTP secret & buộc bật lại 2FA")
def reset_otp_secret(modeladmin, request, queryset):
    count = 0
    for user in queryset:
        user.otp_secret = create_otp_secret()
        user.is_2fa_enabled = False
        user.must_setup_2fa = True
        user.save()
        count += 1
    messages.success(
        request,
        f"Đã reset OTP cho {count} user. Họ sẽ phải quét mã OTP mới khi đăng nhập."
    )

@admin.action(description="Bật cờ 'bắt buộc 2FA' cho user được chọn")
def force_require_2fa(modeladmin, request, queryset):
    updated = queryset.update(must_setup_2fa=True)
    messages.success(
        request,
        f"Đã bật ép buộc 2FA cho {updated} user được chọn."
    )

@admin.action(description="Tắt cờ 'bắt buộc 2FA' cho user được chọn")
def disable_require_2fa(modeladmin, request, queryset):
    updated = queryset.update(must_setup_2fa=False)
    messages.success(
        request,
        f"Đã tắt ép buộc 2FA cho {updated} user được chọn."
    )

@admin.action(description="Vô hiệu hoá 2FA hiện tại (tắt is_2fa_enabled)")
def disable_2fa(modeladmin, request, queryset):
    updated = queryset.update(is_2fa_enabled=False)
    messages.success(
        request,
        f"Đã tắt 2FA cho {updated} user được chọn."
    )


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Thông tin cá nhân", {"fields": ("first_name", "last_name", "email")}),
        ("Quyền hệ thống", {
            "fields": (
                "role",
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Trạng thái bảo mật / 2FA", {
            "fields": (
                "email_verified",
                "otp_secret",
                "is_2fa_enabled",
                "must_setup_2fa",
            )
        }),
        ("Dấu thời gian", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username",
                "email",
                "password1",
                "password2",
                "role",
                "is_staff",
                "is_superuser",
                "must_setup_2fa",
            ),
        }),
    )

    list_display = (
        "username",
        "email",
        "role",
        "email_verified",
        "is_2fa_enabled",
        "must_setup_2fa",
        "is_staff",
        "is_superuser",
    )

    list_filter = (
        "role",
        "email_verified",
        "is_2fa_enabled",
        "must_setup_2fa",
        "is_staff",
        "is_superuser",
        "is_active",
    )

    search_fields = ("username", "email")
    ordering = ("username",)

    actions = [
        reset_otp_secret,
        force_require_2fa,
        disable_require_2fa,
        disable_2fa,
    ]


# ----- ADMIN CHO SECURITYPOLICY -----

@admin.register(SecurityPolicy)
class SecurityPolicyAdmin(admin.ModelAdmin):
    list_display = ("require_2fa_for_new_users", "updated_at")

    # 2 "nút tổng" để ép tất cả user
    actions = ["force_all_users_require_2fa", "disable_all_users_require_2fa"]

    @admin.action(description="Ép TOÀN BỘ user phải bật lại 2FA (must_setup_2fa=True)")
    def force_all_users_require_2fa(self, request, queryset):
        # ép tất cả user (kể cả không nằm trong queryset, để làm 'nút tổng')
        updated = User.objects.update(must_setup_2fa=True)
        messages.success(
            request,
            f"Đã ép {updated} user phải bật 2FA. Lần đăng nhập tới ai chưa bật sẽ bị bắt quét OTP."
        )

    @admin.action(description="Bỏ ép buộc 2FA cho TOÀN BỘ user (must_setup_2fa=False)")
    def disable_all_users_require_2fa(self, request, queryset):
        updated = User.objects.update(must_setup_2fa=False)
        messages.success(
            request,
            f"Đã bỏ ép buộc 2FA cho {updated} user. Người dùng có thể đăng nhập không cần setup OTP ngay."
        )
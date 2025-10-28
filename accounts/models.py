from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("STAFF", "Staff"),
        ("USER", "User"),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="USER")

    email_verified = models.BooleanField(default=False)

    # 2FA / OTP
    otp_secret = models.CharField(max_length=64, blank=True, null=True)
    is_2fa_enabled = models.BooleanField(default=False)

    # ép buộc người dùng phải bật 2FA trước khi được dùng hệ thống
    must_setup_2fa = models.BooleanField(
        default=True,
        help_text="Nếu True: user bị ép phải quét QR và bật OTP trước khi dùng hệ thống."
    )

    def is_admin(self):
        return self.role == "ADMIN"

    def is_staff_role(self):
        return self.role in ["ADMIN", "STAFF"]


class SecurityPolicy(models.Model):
    """
    Chính sách bảo mật cấp hệ thống.
    Chỉ cần 1 record duy nhất dùng chung cho toàn site.
    Admin chỉnh ở trang /admin/.
    """
    require_2fa_for_new_users = models.BooleanField(
        default=True,
        help_text="Nếu bật: tài khoản mới tạo sẽ bị ép phải setup 2FA ngay lần đầu đăng nhập."
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Chính sách bảo mật hệ thống"

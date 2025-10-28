from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


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

    # user có bị bắt buộc phải setup 2FA trước khi xài hệ thống không
    must_setup_2fa = models.BooleanField(
        default=True,
        help_text="Nếu True: user bị ép phải quét QR và bật OTP trước khi dùng hệ thống."
    )

    # bảo vệ brute-force OTP
    failed_otp_attempts = models.IntegerField(default=0)
    otp_locked = models.BooleanField(
        default=False,
        help_text="True = tạm khóa giai đoạn OTP vì nhập sai quá nhiều lần."
    )

    # ép đổi mật khẩu (sau sự cố bảo mật)
    must_change_password = models.BooleanField(
        default=False,
        help_text="True = user sẽ bị chuyển sang trang đổi mật khẩu trước khi vào dashboard."
    )

    def is_admin(self):
        return self.role == "ADMIN"

    def is_staff_role(self):
        return self.role in ["ADMIN", "STAFF"]


class SecurityPolicy(models.Model):
    """
    Chính sách bảo mật cấp hệ thống (chỉ cần 1 record).
    - require_2fa_for_new_users: nếu bật thì user mới đăng ký sẽ must_setup_2fa=True
    """
    require_2fa_for_new_users = models.BooleanField(
        default=True,
        help_text="Nếu bật: tài khoản mới tạo sẽ bị ép phải setup 2FA ngay lần đầu đăng nhập."
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Chính sách bảo mật hệ thống"


class SecurityLog(models.Model):
    """
    Nhật ký bảo mật: ai đăng nhập, OTP sai, tài khoản bị khóa OTP, v.v.
    Admin có thể xem trong trang admin.
    """
    EVENT_CHOICES = (
        ("LOGIN_SUCCESS", "LOGIN_SUCCESS"),
        ("OTP_SUCCESS", "OTP_SUCCESS"),
        ("OTP_FAIL", "OTP_FAIL"),
        ("OTP_LOCKED", "OTP_LOCKED"),
        ("FORCED_2FA", "FORCED_2FA"),
        ("RESET_OTP", "RESET_OTP"),
        ("FORCE_PW_RESET", "FORCE_PW_RESET"),
    )

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    event = models.CharField(max_length=32, choices=EVENT_CHOICES)
    ip = models.CharField(max_length=64, blank=True)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        who = self.user.username if self.user else "unknown-user"
        return f"{self.created_at} {who} {self.event}"

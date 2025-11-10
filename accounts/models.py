from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
import secrets

class User(AbstractUser):
    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("STAFF", "Staff"),
        ("USER", "User"),
    )
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True, default="avatars/default.png")
    bio = models.TextField(blank=True, null=True, help_text="Giới thiệu ngắn về bạn")
    email = models.EmailField("email address", unique=True)

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="USER")
    email_verified = models.BooleanField(default=False)

    # 2FA / OTP
    otp_secret = models.CharField(max_length=64, blank=True, null=True)
    is_2fa_enabled = models.BooleanField(default=False)

    must_setup_2fa = models.BooleanField(
        default=True,
        help_text="Nếu True: user bị ép phải quét QR và bật OTP trước khi dùng hệ thống."
    )

    failed_otp_attempts = models.IntegerField(default=0)
    otp_locked = models.BooleanField(
        default=False,
        help_text="True = tạm khóa giai đoạn OTP vì nhập sai quá nhiều lần."
    )

    must_change_password = models.BooleanField(
        default=False,
        help_text="True = user sẽ bị chuyển sang trang đổi mật khẩu trước khi vào dashboard."
    )

    def is_admin(self):
        return self.role == "ADMIN"

    def is_staff_role(self):
        return self.role in ["ADMIN", "STAFF"]
    
    def generate_backup_codes(self):
        """
        Tạo và lưu 10 mã khôi phục.
        Trả về danh sách các mã (plaintext) để hiển thị cho user 1 LẦN.
        """
        # Xóa các mã cũ
        BackupCode.objects.filter(user=self).delete()
        
        plaintext_codes = []
        codes_to_create = []

        for _ in range(10):
            # Tạo mã 8 ký tự (VD: abcd-1234)
            code = f"{secrets.token_hex(2)}-{secrets.token_hex(2)}" 
            plaintext_codes.append(code)
            
            hashed_code = make_password(code) # Hash mã
            codes_to_create.append(
                BackupCode(user=self, code_hash=hashed_code, is_used=False)
            )

        BackupCode.objects.bulk_create(codes_to_create)
        return plaintext_codes

    def verify_backup_code(self, code: str) -> bool:
        """
        Kiểm tra một mã khôi phục (plaintext) có hợp lệ và chưa dùng không.
        Nếu OK, đánh dấu là đã dùng.
        """
        unused_codes = BackupCode.objects.filter(user=self, is_used=False)
        for backup_code in unused_codes:
            if check_password(code, backup_code.code_hash):
                backup_code.is_used = True
                backup_code.save()
                return True
        return False


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
        # Thêm 2 event mới
        ("EMAIL_OTP_SENT", "EMAIL_OTP_SENT"),
        ("BACKUP_CODE_USED", "BACKUP_CODE_USED"),
    )

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    event = models.CharField(max_length=32, choices=EVENT_CHOICES)
    ip = models.CharField(max_length=64, blank=True)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        who = self.user.username if self.user else "unknown-user"
        return f"{self.created_at} {who} {self.event}"

# Cấu hình bảo mật toàn cục (singleton)
class SecurityConfig(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True, default=1, editable=False)
    enforce_2fa = models.BooleanField(default=False, help_text="Bắt buộc tất cả tài khoản phải bật 2FA")
    otp_digits = models.PositiveSmallIntegerField(default=6)
    otp_period = models.PositiveSmallIntegerField(default=30)
    lockout_threshold = models.PositiveSmallIntegerField(default=5, help_text="Sai OTP tối đa trước khi khoá")

    def __str__(self):
        return "Security Config (global)"

    def save(self, *args, **kwargs):
        self.id = 1  # luôn là 1 (singleton)
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj

# ----------------------------------
# MODEL MỚI CHO MÃ KHÔI PHỤC
# ----------------------------------
class BackupCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="backup_codes")
    code_hash = models.CharField(max_length=128, help_text="Mã khôi phục đã được hash")
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Backup code for {self.user.username} (Used: {self.is_used})"
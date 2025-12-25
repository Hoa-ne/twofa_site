from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
# Import thư viện mã hóa
from cryptography.fernet import Fernet
import secrets

class User(AbstractUser):
    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("STAFF", "Staff"),
        ("USER", "User"),
    )
    
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True, default="avatars/default.png", verbose_name="Ảnh đại diện")
    bio = models.TextField(blank=True, null=True, help_text="Giới thiệu ngắn về bạn", verbose_name="Tiểu sử")
    
    # --- PHẦN NICKNAME (Giữ nguyên) ---
    nickname = models.CharField(max_length=50, blank=True, null=True, verbose_name="Biệt danh hiển thị")
    allow_email_otp = models.BooleanField(
        default=True, 
        verbose_name="Cho phép nhận OTP qua Email",
        help_text="Nếu bỏ chọn: User chỉ được dùng App Authenticator, không được bấm nút 'Gửi qua Email'."
    )
    def get_display_name(self):
        """
        Thứ tự ưu tiên hiển thị:
        1. Nickname
        2. Họ tên
        3. Thành viên số [ID]
        """
        if self.nickname:
            return self.nickname
        
        full_name = f"{self.last_name} {self.first_name}".strip()
        if full_name:
            return full_name
        
        return f"Thành viên số {self.pk}"
    
    # Các trường cơ bản khác
    email = models.EmailField("Địa chỉ Email", unique=True) 
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="USER", verbose_name="Vai trò")
    email_verified = models.BooleanField(default=False, verbose_name="Đã xác thực Email")

    # --- [SỬA ĐỔI QUAN TRỌNG] PHẦN BẢO MẬT OTP ---
    
    # 1. Đổi tên trường lưu trữ thành 'encrypted_otp_secret'
    # Tăng độ dài lên 255 để chứa chuỗi mã hóa
    encrypted_otp_secret = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name="Mã OTP (Đã mã hóa)"
    )
    
    is_2fa_enabled = models.BooleanField(default=False, verbose_name="Đã bật 2FA")

    # 2. Tạo thuộc tính ảo 'otp_secret' để tự động Mã hóa / Giải mã
    @property
    def otp_secret(self):
        """
        Khi code gọi user.otp_secret: Tự động giải mã từ encrypted_otp_secret
        """
        if not self.encrypted_otp_secret:
            return None
        try:
            # Lấy key từ settings (đã cấu hình từ .env)
            key = settings.OTP_ENCRYPTION_KEY.encode()
            f = Fernet(key)
            # Giải mã
            decrypted_data = f.decrypt(self.encrypted_otp_secret.encode())
            return decrypted_data.decode()
        except Exception:
            return None

    @otp_secret.setter
    def otp_secret(self, value):
        """
        Khi code gán user.otp_secret = "abc": Tự động mã hóa rồi lưu vào encrypted_otp_secret
        """
        if value:
            key = settings.OTP_ENCRYPTION_KEY.encode()
            f = Fernet(key)
            # Mã hóa
            encrypted_data = f.encrypt(value.encode())
            self.encrypted_otp_secret = encrypted_data.decode()
        else:
            self.encrypted_otp_secret = None

    # ---------------------------------------------

    must_setup_2fa = models.BooleanField(
        default=True,
        verbose_name="Bắt buộc thiết lập 2FA",
        help_text="Nếu chọn: Người dùng bị ép phải quét mã QR và bật OTP trước khi dùng hệ thống."
    )

    failed_otp_attempts = models.IntegerField(default=0, verbose_name="Số lần nhập sai OTP")
    
    otp_locked = models.BooleanField(
        default=False,
        verbose_name="Đang bị khóa OTP",
        help_text="Nếu chọn: Tạm khóa tính năng nhập OTP do người dùng nhập sai quá nhiều lần."
    )

    must_change_password = models.BooleanField(
        default=False,
        verbose_name="Yêu cầu đổi mật khẩu",
        help_text="Nếu chọn: Người dùng sẽ bị chuyển sang trang đổi mật khẩu ở lần đăng nhập tới."
    )

    def is_admin(self):
        return self.role == "ADMIN"

    def is_staff_role(self):
        return self.role in ["ADMIN", "STAFF"]
    
    def generate_backup_codes(self):
        # Xóa các mã cũ
        BackupCode.objects.filter(user=self).delete()
        
        plaintext_codes = []
        codes_to_create = []

        for _ in range(10):
            code = f"{secrets.token_hex(2)}-{secrets.token_hex(2)}" 
            plaintext_codes.append(code)
            hashed_code = make_password(code)
            codes_to_create.append(
                BackupCode(user=self, code_hash=hashed_code, is_used=False)
            )

        BackupCode.objects.bulk_create(codes_to_create)
        return plaintext_codes

    def verify_backup_code(self, code: str) -> bool:
        unused_codes = BackupCode.objects.filter(user=self, is_used=False)
        for backup_code in unused_codes:
            if check_password(code, backup_code.code_hash):
                backup_code.is_used = True
                backup_code.save()
                return True
        return False

    class Meta:
        verbose_name = "Người dùng"
        verbose_name_plural = "Danh sách người dùng"


class SecurityPolicy(models.Model):
    require_2fa_for_new_users = models.BooleanField(
        default=True,
        verbose_name="Yêu cầu 2FA cho người dùng mới",
        help_text="Nếu bật: tài khoản mới tạo sẽ bị ép phải setup 2FA ngay lần đầu đăng nhập."
    )

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Cập nhật lần cuối")

    def __str__(self):
        return "Chính sách bảo mật hệ thống"
    
    class Meta:
        verbose_name = "Chính sách bảo mật"
        verbose_name_plural = "Chính sách bảo mật"


class SecurityLog(models.Model):
    EVENT_CHOICES = (
        ("LOGIN_SUCCESS", "LOGIN_SUCCESS"),
        ("OTP_SUCCESS", "OTP_SUCCESS"),
        ("OTP_FAIL", "OTP_FAIL"),
        ("OTP_LOCKED", "OTP_LOCKED"),
        ("FORCED_2FA", "FORCED_2FA"),
        ("RESET_OTP", "RESET_OTP"),
        ("FORCE_PW_RESET", "FORCE_PW_RESET"),
        ("EMAIL_OTP_SENT", "EMAIL_OTP_SENT"),
        ("BACKUP_CODE_USED", "BACKUP_CODE_USED"),
        ("PASSWORD_CHANGED", "PASSWORD_CHANGED"),
        ("ENABLE_2FA", "ENABLE_2FA"),
        ("DISABLE_2FA", "DISABLE_2FA"),
    )
    user_agent = models.CharField(max_length=255, blank=True, null=True, help_text="Thông tin thiết bị/trình duyệt", verbose_name="User Agent")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Người dùng")
    event_type = models.CharField(max_length=32, choices=EVENT_CHOICES, db_column="event", null=True, verbose_name="Loại sự kiện")
    ip = models.CharField(max_length=64, blank=True, verbose_name="Địa chỉ IP")
    note = models.TextField(blank=True, verbose_name="Ghi chú")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Thời gian")

    def __str__(self):
        who = self.user.username if self.user else "unknown-user"
        return f"{self.created_at} {who} {self.event_type}"
    
    class Meta:
        verbose_name = "Nhật ký bảo mật"
        verbose_name_plural = "Nhật ký bảo mật"


# accounts/models.py

class SecurityConfig(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True, default=1, editable=False)
    
    enforce_for_admin = models.BooleanField(
        default=True, 
        verbose_name="Bắt buộc 2FA với Admin", 
        help_text="Bắt buộc tài khoản có quyền Admin/Superuser phải bật 2FA"
    )
    enforce_for_staff = models.BooleanField(
        default=False, 
        verbose_name="Bắt buộc 2FA với NhanVien", 
        help_text="Bắt buộc tài khoản nhân viên NhanVien phải bật 2FA"
    )
    enforce_for_user = models.BooleanField(
        default=False, 
        verbose_name="Bắt buộc 2FA với User", 
        help_text="Bắt buộc người dùng thường phải bật 2FA"
    )

    # --- Cấu hình OTP Email toàn hệ thống ---
    allow_email_otp_system = models.BooleanField(
        default=True,
        verbose_name="Cho phép OTP qua Email (Toàn hệ thống)",
        help_text="Nếu tắt: Không ai được dùng Email để nhận OTP, bắt buộc dùng App (Google Auth)."
    )

    # --- [SỬA ĐỔI] Thêm choices cho độ dài OTP ---
    OTP_DIGITS_CHOICES = (
        (6, "6 chữ số "),
        (8, "8 chữ số "),
    )
    
    otp_digits = models.PositiveSmallIntegerField(
        default=6, 
        verbose_name="Độ dài OTP",
        choices=OTP_DIGITS_CHOICES  # <--- Thêm dòng này để tạo menu chọn
    )
    
    otp_period = models.PositiveSmallIntegerField(default=30, verbose_name="Chu kỳ OTP (giây)")
    lockout_threshold = models.PositiveSmallIntegerField(default=5, verbose_name="Ngưỡng khóa (lần sai)", help_text="Sai OTP tối đa trước khi khoá")

    def __str__(self):
        return "Cấu hình bảo mật "

    def save(self, *args, **kwargs):
        self.id = 1 
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj
    
    class Meta:
        verbose_name = "Cấu hình bảo mật"
        verbose_name_plural = "Cấu hình bảo mật"


class BackupCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="backup_codes", verbose_name="Người dùng")
    code_hash = models.CharField(max_length=128, help_text="Mã khôi phục đã được hash", verbose_name="Mã Hash")
    is_used = models.BooleanField(default=False, verbose_name="Đã sử dụng")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")

    def __str__(self):
        return f"Backup code for {self.user.username} (Used: {self.is_used})"
    
    class Meta:
        verbose_name = "Mã khôi phục"
        verbose_name_plural = "Mã khôi phục"
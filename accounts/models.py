from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from cryptography.fernet import Fernet
import secrets

# Mo hinh nguoi dung tuy chinh ke thua tu AbstractUser cua Django
class User(AbstractUser):
    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("STAFF", "Staff"),
        ("USER", "User"),
    )
    
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True, default="avatars/default.png", verbose_name="Ảnh đại diện")
    bio = models.TextField(blank=True, null=True, help_text="Giới thiệu ngắn về bạn", verbose_name="Tiểu sử")
    
    nickname = models.CharField(max_length=50, blank=True, null=True, verbose_name="Biệt danh hiển thị")
    allow_email_otp = models.BooleanField(
        default=True, 
        verbose_name="Cho phép nhận OTP qua Email",
        help_text="Nếu bỏ chọn: User chỉ được dùng App Authenticator, không được bấm nút 'Gửi qua Email'."
    )

    # Xac dinh ten hien thi uu tien theo thu tu: nickname -> ho ten -> ID thanh vien
    def get_display_name(self):
        if self.nickname:
            return self.nickname
        
        full_name = f"{self.last_name} {self.first_name}".strip()
        if full_name:
            return full_name
        
        return f"Thành viên số {self.pk}"
    
    email = models.EmailField("Địa chỉ Email", unique=True) 
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="USER", verbose_name="Vai trò")
    email_verified = models.BooleanField(default=False, verbose_name="Đã xác thực Email")

    encrypted_otp_secret = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name="Mã OTP (Đã mã hóa)"
    )
    
    is_2fa_enabled = models.BooleanField(default=False, verbose_name="Đã bật 2FA")

    @property
    # Tu dong giai ma OTP secret khi duoc truy xuat
    def otp_secret(self):
        if not self.encrypted_otp_secret:
            return None
        try:
            key = settings.OTP_ENCRYPTION_KEY.encode()
            f = Fernet(key)
            decrypted_data = f.decrypt(self.encrypted_otp_secret.encode())
            return decrypted_data.decode()
        except Exception:
            return None

    @otp_secret.setter
    # Tu dong ma hoa OTP secret truoc khi luu vao co so du lieu
    def otp_secret(self, value):
        if value:
            key = settings.OTP_ENCRYPTION_KEY.encode()
            f = Fernet(key)
            encrypted_data = f.encrypt(value.encode())
            self.encrypted_otp_secret = encrypted_data.decode()
        else:
            self.encrypted_otp_secret = None

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

    # Kiem tra nguoi dung co phai la quan tri vien khong
    def is_admin(self):
        return self.role == "ADMIN"

    # Kiem tra nguoi dung co thuoc nhom nhan vien quan ly khong
    def is_staff_role(self):
        return self.role in ["ADMIN", "STAFF"]
    
    # Tao moi danh sach ma du phong va luu duoi dang ma hoa hash
    def generate_backup_codes(self):
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

    # Kiem tra ma du phong nguoi dung nhap vao co hop le va chua su dung khong
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


# Mo hinh luu tru chinh sach bao mat chung cua he thong
class SecurityPolicy(models.Model):
    require_2fa_for_new_users = models.BooleanField(
        default=True,
        verbose_name="Yêu cầu 2FA cho người dùng mới",
        help_text="Nếu bật: tài khoản mới tạo sẽ bị ép phải setup 2FA ngay lần đầu đăng nhập."
    )

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Cập nhật lần cuối")

    # Tra ve ten hien thi dai dien cho chinh sach bao mat
    def __str__(self):
        return "Chính sách bảo mật hệ thống"
    
    class Meta:
        verbose_name = "Chính sách bảo mật"
        verbose_name_plural = "Chính sách bảo mật"


# Mo hinh ghi lai nhat ky cac su kien lien quan den bao mat
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

    # Tra ve chuoi mo ta ngan gon ve su kien bao mat
    def __str__(self):
        who = self.user.username if self.user else "unknown-user"
        return f"{self.created_at} {who} {self.event_type}"
    
    class Meta:
        verbose_name = "Nhật ký bảo mật"
        verbose_name_plural = "Nhật ký bảo mật"


# Mo hinh cau hinh cac thong so bao mat cho toan he thong
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

    allow_email_otp_system = models.BooleanField(
        default=True,
        verbose_name="Cho phép OTP qua Email (Toàn hệ thống)",
        help_text="Nếu tắt: Không ai được dùng Email để nhận OTP, bắt buộc dùng App (Google Auth)."
    )

    OTP_DIGITS_CHOICES = (
        (6, "6 chữ số "),
        (8, "8 chữ số "),
    )
    
    otp_digits = models.PositiveSmallIntegerField(
        default=6, 
        verbose_name="Độ dài OTP",
        choices=OTP_DIGITS_CHOICES
    )
    
    otp_period = models.PositiveSmallIntegerField(default=30, verbose_name="Chu kỳ OTP (giây)")
    lockout_threshold = models.PositiveSmallIntegerField(default=5, verbose_name="Ngưỡng khóa (lần sai)", help_text="Sai OTP tối đa trước khi khoá")

    # Tra ve ten mac dinh cua cau hinh bao mat
    def __str__(self):
        return "Cấu hình bảo mật "

    # Dam bao chi co mot ban ghi cau hinh duy nhat luon co ID la 1
    def save(self, *args, **kwargs):
        self.id = 1 
        super().save(*args, **kwargs)

    @classmethod
    # Lay ra doi tuong cau hinh duy nhat cua he thong
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj
    
    class Meta:
        verbose_name = "Cấu hình bảo mật"
        verbose_name_plural = "Cấu hình bảo mật"


# Mo hinh luu tru ma du phong cho nguoi dung duoi dang hash
class BackupCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="backup_codes", verbose_name="Người dùng")
    code_hash = models.CharField(max_length=128, help_text="Mã khôi phục đã được hash", verbose_name="Mã Hash")
    is_used = models.BooleanField(default=False, verbose_name="Đã sử dụng")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")

    # Tra ve thong tin tom tat cua ma du phong
    def __str__(self):
        return f"Backup code for {self.user.username} (Used: {self.is_used})"
    
    class Meta:
        verbose_name = "Mã khôi phục"
        verbose_name_plural = "Mã khôi phục"
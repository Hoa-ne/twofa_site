from django.test import TestCase
from django.contrib.auth import get_user_model
from .otp_algo import totp, verify_totp 
from .models import SecurityConfig

User = get_user_model()

class DynamicSecurityConfigTestCase(TestCase):
    """Test kiểm tra tính năng thay đổi cấu hình OTP động"""

    def setUp(self):
        # Tạo user mẫu
        self.user = User.objects.create_user(username="test_config", password="password")
        self.user.otp_secret = "JBSWY3DPEHPK3PXP" # Secret mẫu
        self.user.save()
        
        # Đảm bảo config luôn reset về mặc định trước mỗi bài test
        self.config = SecurityConfig.get_solo()
        self.config.otp_digits = 6
        self.config.otp_period = 30
        self.config.save()

    def test_default_config_6_digits(self):
        """1. Kiểm tra mặc định là 6 số"""
        # Sinh mã theo chuẩn 6 số
        code_6 = totp(self.user.otp_secret, digits=6, period=30)
        
        # Verify bằng tham số lấy từ DB
        is_valid = verify_totp(
            self.user.otp_secret, 
            code_6, 
            digits=self.config.otp_digits,   # Lấy từ DB (đang là 6)
            period=self.config.otp_period    # Lấy từ DB (đang là 30)
        )
        
        self.assertEqual(len(code_6), 6)
        self.assertTrue(is_valid, "Mặc định phải verify được mã 6 số")

    def test_change_to_8_digits(self):
        """2. Kiểm tra khi Admin đổi sang 8 số"""
        # --- GIẢ LẬP ADMIN ĐỔI CẤU HÌNH ---
        self.config.otp_digits = 8
        self.config.save()
        
        # Sinh mã 8 số
        code_8 = totp(self.user.otp_secret, digits=8, period=30)
        
        # Sinh mã 6 số (cũ)
        code_6 = totp(self.user.otp_secret, digits=6, period=30)

        # Kiểm tra độ dài
        self.assertEqual(len(code_8), 8)

        # Verify mã 8 số -> Phải ĐÚNG
        valid_8 = verify_totp(
            self.user.otp_secret, 
            code_8, 
            digits=self.config.otp_digits, # DB đang là 8
            period=self.config.otp_period
        )
        self.assertTrue(valid_8, "Sau khi đổi config, hệ thống phải nhận mã 8 số")

        # Verify mã 6 số -> Phải SAI
        valid_6 = verify_totp(
            self.user.otp_secret, 
            code_6, 
            digits=self.config.otp_digits, # DB đang là 8
            period=self.config.otp_period
        )
        self.assertFalse(valid_6, "Hệ thống 8 số không được chấp nhận mã 6 số")

    def test_change_period_60s(self):
        """3. Kiểm tra khi Admin đổi chu kỳ lên 60 giây"""
        # --- GIẢ LẬP ADMIN ĐỔI CẤU HÌNH ---
        self.config.otp_period = 60
        self.config.save()
        
        # Sinh mã theo chu kỳ 60s
        code_60s = totp(self.user.otp_secret, digits=6, period=60)
        
        # Verify
        is_valid = verify_totp(
            self.user.otp_secret, 
            code_60s, 
            digits=self.config.otp_digits,
            period=self.config.otp_period # DB đang là 60
        )
        self.assertTrue(is_valid, "Phải verify được mã sinh ra từ chu kỳ 60s")
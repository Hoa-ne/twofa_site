from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User

# MỚI: Import form admin mặc định
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# --- FORM MỚI CHO ADMIN ---
# Form này dùng khi BẤM NÚT "ADD USER"
class UserAdminCreationForm(UserCreationForm):
    class Meta:
        model = User
        # Thêm các trường bạn muốn thấy trên trang "Add user"
        fields = ("username", "email", "role", "is_staff", "is_superuser", "must_setup_2fa")

    # SỬA LẠI HÀM SAVE NÀY (ĐÂY LÀ PHẦN SỬA QUAN TRỌNG)
    def save(self, commit=True):
        # 1. Lấy user object từ form cha (chỉ có username, password)
        user = super().save(commit=False) 
        
        # 2. THÊM DỮ LIỆU TỪ CÁC TRƯỜNG MỚI CỦA CHÚNG TA (bước bị thiếu)
        user.email = self.cleaned_data["email"]
        user.role = self.cleaned_data["role"]
        user.is_staff = self.cleaned_data["is_staff"]
        user.is_superuser = self.cleaned_data["is_superuser"]
        user.must_setup_2fa = self.cleaned_data["must_setup_2fa"]
        
        # 3. Đặt các giá trị mặc định
        user.email_verified = True # Khi Admin tạo, cho phép xác thực email luôn
        
        # 4. Lưu vào DB
        if commit:
            user.save()
        return user


# Form này dùng khi BẤM VÀO SỬA 1 USER CÓ SẴN
class UserAdminChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__' # Hiển thị tất cả các trường

# --- CÁC FORM CŨ (CỦA USER) ---

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Mật khẩu",
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Mật khẩu"
        })
    )
    password2 = forms.CharField(
        label="Nhập lại mật khẩu",
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Nhập lại mật khẩu"
        })
    )

    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Tên đăng nhập"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-input",
                "placeholder": "Email"
            }),
        }

    def clean_password2(self):
        pw1 = self.cleaned_data.get("password1")
        pw2 = self.cleaned_data.get("password2")
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("Hai mật khẩu không khớp.")
        # validate độ mạnh mật khẩu (Django built-in rules)
        validate_password(pw1)
        return pw2

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip()
        # SỬA: Cho phép admin chỉnh sửa user mà không báo lỗi email (chỉ check khi đăng ký)
        # Bỏ qua check email trùng lặp ở đây, UserAdminCreationForm sẽ tự xử lý
        if self.instance.pk is None and User.objects.filter(email__iexact=email).exists():
             raise ValidationError("Email đã tồn tại trong hệ thống.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        pw = self.cleaned_data["password1"]
        user.set_password(pw)
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Tên đăng nhập",
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "Tên đăng nhập" # <-- SỬA TỪ "Username"
        })
    )
    password = forms.CharField(
        label="Mật khẩu",
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Mật khẩu"
        })
    )

    def clean(self):
        cleaned = super().clean()
        username = cleaned.get("username")
        password = cleaned.get("password")

        if not username or not password:
            return cleaned

        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("Sai tài khoản hoặc mật khẩu.")

        # chặn đăng nhập nếu email chưa verify
        if not user.email_verified:
            raise forms.ValidationError("Email chưa được xác thực. Vui lòng kiểm tra hộp thư.")

        if not user.is_active:
            raise forms.ValidationError("Tài khoản đã bị vô hiệu hoá.")

        cleaned["user"] = user
        return cleaned


class OTPForm(forms.Form):
    # ... (giữ nguyên form OTPForm) ...
    otp_code = forms.CharField(
        label="Mã OTP",
        max_length=8, 
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "Nhập mã OTP 6 số"
        })
    )
    
    remember_me = forms.BooleanField(
        label="Tin cậy thiết bị này trong 30 ngày",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )


class Enable2FAConfirmForm(forms.Form):
    # ... (giữ nguyên form Enable2FAConfirmForm) ...
    otp_code = forms.CharField(
        label="Mã OTP",
        max_length=6,
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "Nhập mã OTP từ ứng dụng Authenticator"
        })
    )


class ChangePasswordForm(forms.Form):
    # ... (giữ nguyên form ChangePasswordForm) ...
    old_password = forms.CharField(
        label="Mật khẩu hiện tại",
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Mật khẩu hiện tại"
        })
    )
    new_password1 = forms.CharField(
        label="Mật khẩu mới",
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Mật khẩu mới"
        })
    )
    new_password2 = forms.CharField(
        label="Nhập lại mật khẩu mới",
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Nhập lại mật khẩu mới"
        })
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_old_password(self):
        old = self.cleaned_data["old_password"]
        if not self.user.check_password(old):
            raise forms.ValidationError("Mật khẩu hiện tại không đúng.")
        return old

    def clean(self):
        cleaned = super().clean()
        pw1 = cleaned.get("new_password1")
        pw2 = cleaned.get("new_password2")

        if pw1 and pw2 and pw1 != pw2:
            self.add_error("new_password2", "Hai mật khẩu mới không khớp.")

        if pw1:
            validate_password(pw1, user=self.user)

        return cleaned

class BackupCodeForm(forms.Form):
    # ... (giữ nguyên form BackupCodeForm) ...
    code = forms.CharField(
        label="Mã khôi phục",
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "VD: abcd-1234"
        })
    )
    
    remember_me = forms.BooleanField(
        label="Tin cậy thiết bị này trong 30 ngày",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )
    
class ProfileEditForm(forms.ModelForm):
    # ... (giữ nguyên form ProfileEditForm) ...
    class Meta:
        model = User
        fields = ["avatar", "bio"]
        widgets = {
            "bio": forms.Textarea(attrs={
                "class": "form-input",
                "rows": 3,
                "placeholder": "Giới thiệu ngắn về bạn..."
            }),
            "avatar": forms.ClearableFileInput(attrs={
                "class": "form-input",
            })
        }
        labels = {
            "avatar": "Ảnh đại diện (Avatar)",
            "bio": "Tiểu sử (Bio)",
        }

class Disable2FAForm(forms.Form):
    """
    Form yêu cầu mật khẩu và OTP để xác nhận tắt 2FA.
    """
    password = forms.CharField(
        label="Mật khẩu hiện tại",
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Nhập mật khẩu của bạn"
        })
    )
    otp_code = forms.CharField(
        label="Mã OTP (từ ứng dụng)",
        max_length=8, 
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "Nhập mã OTP 6 số"
        })
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not self.user.check_password(password):
            raise forms.ValidationError("Mật khẩu không đúng.")
        return password
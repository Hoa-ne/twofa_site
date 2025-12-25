from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User
from .models import SecurityConfig

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User, SecurityConfig, SecurityLog, BackupCode

# Form tao nguoi dung moi trong trang Admin voi cac truong tuy chinh
class UserAdminCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "role", "is_staff", "is_superuser", "must_setup_2fa")

    # Luu thong tin nguoi dung moi va cac thiet lap quyen han vao co so du lieu
    def save(self, commit=True):
        user = super().save(commit=False) 
        
        user.email = self.cleaned_data["email"]
        user.role = self.cleaned_data["role"]
        user.is_staff = self.cleaned_data["is_staff"]
        user.is_superuser = self.cleaned_data["is_superuser"]
        user.must_setup_2fa = self.cleaned_data["must_setup_2fa"]
        
        user.email_verified = True 
        
        if commit:
            user.save()
        return user


# Form chinh sua toan bo thong tin nguoi dung trong trang Admin
class UserAdminChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


# Form dang ky tai khoan nguoi dung moi phia giao dien chinh
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
        fields = ["username", "email", "nickname"] 
        
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Tên đăng nhập"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-input",
                "placeholder": "Email"
            }),
            "nickname": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Biệt danh (VD: Siêu Nhân)"
            }),
        }
        help_texts = {
            'username': '',
        }

    # Kiem tra va loai bo cac biet danh chua tu khoa nhay cam hoac cam ki
    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname', '').strip()
        
        if not nickname:
            return None

        forbidden_words = [
            'admin', 'admiin', 'administrator', 'quản trị', 'quan tri',
            'mod', 'smod', 'moderator', 
            'support', 'hỗ trợ', 'hotro', 
            'system', 'hệ thống', 'root', 'superuser',
            'bot', 'staff', 'nhân viên'
        ]
        
        lower_nick = nickname.lower()

        for word in forbidden_words:
            if word in lower_nick:
                raise forms.ValidationError(f"Biệt danh không được chứa từ '{word}' để tránh gây nhầm lẫn.")
        
        return nickname

    # Xac thuc mat khau nhap lai co trung khop voi mat khau chinh hay khong
    def clean_password2(self):
        pw1 = self.cleaned_data.get("password1")
        pw2 = self.cleaned_data.get("password2")
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("Hai mật khẩu không khớp.")
        validate_password(pw1)
        return pw2

    # Kiem tra xem dia chi email da ton tai trong he thong hay chua
    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip()
        if self.instance.pk is None and User.objects.filter(email__iexact=email).exists():
             raise ValidationError("Email đã tồn tại trong hệ thống.")
        return email

    # Thiet lap mat khau cho nguoi dung va luu vao co so du lieu
    def save(self, commit=True):
        user = super().save(commit=False)
        pw = self.cleaned_data["password1"]
        user.set_password(pw)
        if commit:
            user.save()
        return user


# Form dang nhap he thong va kiem tra trang thai tai khoan
class LoginForm(forms.Form):
    username = forms.CharField(
        label="Tên đăng nhập",
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "Tên đăng nhập" 
        })
    )
    password = forms.CharField(
        label="Mật khẩu",
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Mật khẩu"
        })
    )

    # Xac thuc thong tin dang nhap va kiem tra trang thai hoat dong cua tai khoan
    def clean(self):
        cleaned = super().clean()
        username = cleaned.get("username")
        password = cleaned.get("password")

        if not username or not password:
            return cleaned

        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("Sai tài khoản hoặc mật khẩu.")

        if not user.email_verified:
            raise forms.ValidationError("Email chưa được xác thực. Vui lòng kiểm tra hộp thư.")

        if not user.is_active:
            raise forms.ValidationError("Tài khoản đã bị vô hiệu hoá.")

        cleaned["user"] = user
        return cleaned


# Form nhap ma xac thuc OTP voi giao dien tuy chinh
class OTPForm(forms.Form):
    otp_code = forms.CharField(
        label="Mã OTP",
        widget=forms.TextInput(attrs={
            'class': 'form-input', 
            'placeholder': 'Nhập mã OTP', 
            'autocomplete': 'off',
            'pattern': '[0-9]*', 
            'inputmode': 'numeric',
            'autofocus': 'autofocus',
            'style': 'letter-spacing: 5px; font-size: 1.2rem; text-align: center;'
        })
    )

    remember_me = forms.BooleanField(
        label="Tin cậy thiết bị này trong 30 ngày",
        required=False,
        widget=forms.CheckboxInput(attrs={
            "class": "form-check-input me-2",
            "style": "cursor: pointer;"
        })
    )

    # Khoi tao form va thiet lap cau hinh do dai ma OTP dong tu co so du lieu
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        try:
            config = SecurityConfig.get_solo()
            digits = config.otp_digits
        except Exception:
            digits = 6 
            
        self.fields['otp_code'].max_length = digits
        self.fields['otp_code'].min_length = digits
        
        self.fields['otp_code'].widget.attrs.update({
            'placeholder': f'Nhập {digits} chữ số',
            'maxlength': str(digits), 
        })


# Form xac nhan ma OTP lan dau de kich hoat tinh nang 2FA
class Enable2FAConfirmForm(forms.Form):
    otp_code = forms.CharField(
        label="Mã OTP",
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "autocomplete": "off",
            "pattern": "[0-9]*",
            "inputmode": "numeric",
        })
    )

    # Khoi tao form xac nhan kich hoat 2FA voi do dai ma OTP tu dong
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        try:
            config = SecurityConfig.get_solo()
            digits = config.otp_digits
        except Exception:
            digits = 6
            
        self.fields['otp_code'].max_length = digits
        self.fields['otp_code'].min_length = digits
        self.fields['otp_code'].widget.attrs.update({
            'placeholder': f'Nhập {digits} chữ số từ ứng dụng',
            'maxlength': str(digits)
        })


# Form thay doi mat khau nguoi dung
class ChangePasswordForm(forms.Form):
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

    # Khoi tao form doi mat khau gan lien voi mot nguoi dung cu the
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    # Kiem tra mat khau cu nguoi dung nhap vao co chinh xac khong
    def clean_old_password(self):
        old = self.cleaned_data["old_password"]
        if not self.user.check_password(old):
            raise forms.ValidationError("Mật khẩu hiện tại không đúng.")
        return old

    # Kiem tra tinh hop le cua hai mat khau moi duoc nhap vao
    def clean(self):
        cleaned = super().clean()
        pw1 = cleaned.get("new_password1")
        pw2 = cleaned.get("new_password2")

        if pw1 and pw2 and pw1 != pw2:
            self.add_error("new_password2", "Hai mật khẩu mới không khớp.")

        if pw1:
            validate_password(pw1, user=self.user)

        return cleaned


# Form su dung ma du phong de dang nhap khi mat thiet bi OTP
class BackupCodeForm(forms.Form):
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
    

# Form chinh sua thong tin ca nhan va ho so nguoi dung
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'nickname', 'first_name', 'last_name', 'bio']
        widgets = {
            "bio": forms.Textarea(attrs={
                "class": "form-input",
                "rows": 3,
                "placeholder": "Giới thiệu ngắn về bạn..."
            }),
            "avatar": forms.ClearableFileInput(attrs={
                "class": "form-input",
            }),
            "nickname": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Biệt danh hiển thị (VD: Siêu Nhân)"
            }),
            "first_name": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Tên"
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Họ"
            }),
        }
        labels = {
            "avatar": "Ảnh đại diện (Avatar)",
            "bio": "Tiểu sử (Bio)",
            "nickname": "Biệt danh (Nickname)",
            "first_name": "Tên",
            "last_name": "Họ",
        }

    # Kiem tra biet danh khi chinh sua ho so de tranh cac tu khoa bi cam
    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname', '').strip()
        if not nickname:
            return None

        forbidden_words = [
            'admin', 'admiin', 'administrator', 'quản trị', 'quan tri',
            'mod', 'smod', 'moderator', 'support', 'hỗ trợ', 'hotro', 
            'system', 'hệ thống', 'root', 'superuser', 'bot', 'staff'
        ]
        
        lower_nick = nickname.lower()
        for word in forbidden_words:
            if word in lower_nick:
                raise forms.ValidationError(f"Biệt danh không được chứa từ '{word}' để tránh gây nhầm lẫn.")
        
        return nickname


# Form xac nhan tat tinh nang bao mat 2 lop bang mat khau hoac ma du phong
class Disable2FAForm(forms.Form):
    password = forms.CharField(
        label="Mật khẩu hiện tại",
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Nhập mật khẩu của bạn"
        })
    )
    
    backup_code = forms.CharField(
        label="Mã dự phòng (Backup Code)",
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "VD: a1b2-c3d4",
            "autocomplete": "off"
        }),
        help_text="Nhập một trong các mã dự phòng bạn đã lưu khi bật 2FA."
    )

    # Khoi tao form tat xac thuc 2 lop gan voi nguoi dung cu the
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    # Xac thuc mat khau nguoi dung truoc khi cho phep tat 2FA
    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not self.user.check_password(password):
            raise forms.ValidationError("Mật khẩu không đúng.")
        return password


# Form xac thuc dia chi email cua nguoi dung
class EmailConfirmationForm(forms.Form):
    email = forms.EmailField(
        label="Nhập địa chỉ Email đăng ký",
        widget=forms.TextInput(attrs={
            'class': 'form-input', 
            'placeholder': 'vd: user@example.com',
            'autofocus': 'autofocus'
        })
    )
    
    # Khoi tao form xac thuc email va luu email goc de so sanh
    def __init__(self, *args, **kwargs):
        self.user_email = kwargs.pop('user_email', None)
        super().__init__(*args, **kwargs)

    # So sanh email nhap vao voi email da dang ky cua tai khoan
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.user_email and email != self.user_email:
            raise forms.ValidationError("Email bạn nhập không khớp với email đăng ký của tài khoản này.")
        return email
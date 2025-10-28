from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User


class RegisterForm(forms.ModelForm):
    """
    Form đăng ký tài khoản mới.
    - Gồm username, email, password1, password2
    - Kiểm tra trùng mật khẩu
    - Dùng set_password khi save()
    """
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

    def save(self, commit=True):
        user = super().save(commit=False)
        pw = self.cleaned_data["password1"]
        user.set_password(pw)
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """
    Form đăng nhập bước 1 (username + password).
    Sau khi clean() thành công, self.cleaned_data["user"] sẽ chứa đối tượng User đã auth.
    """
    username = forms.CharField(
        label="Tên đăng nhập",
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "Username"
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
    """
    Form nhập mã OTP 6 số ở bước 2FA khi login.
    """
    otp_code = forms.CharField(
        label="Mã OTP",
        max_length=6,
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "Nhập mã OTP 6 số"
        })
    )


class Enable2FAConfirmForm(forms.Form):
    """
    Form xác nhận OTP sau khi người dùng quét QR để bật 2FA lần đầu.
    """
    otp_code = forms.CharField(
        label="Mã OTP",
        max_length=6,
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "Nhập mã OTP từ ứng dụng Authenticator"
        })
    )


class ChangePasswordForm(forms.Form):
    """
    Form ép đổi mật khẩu sau sự cố (must_change_password=True).
    - Người dùng phải nhập mật khẩu hiện tại
    - Và đặt mật khẩu mới (2 lần)
    - Có validate_password để đảm bảo độ mạnh
    """
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

        # kiểm tra độ mạnh mật khẩu mới
        if pw1:
            validate_password(pw1, user=self.user)

        return cleaned

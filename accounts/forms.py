from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        user = authenticate(
            username=cleaned.get("username"),
            password=cleaned.get("password"),
        )
        if not user:
            raise forms.ValidationError("Sai tài khoản hoặc mật khẩu.")
        if not user.email_verified:
            raise forms.ValidationError("Email chưa verify. Vui lòng kiểm tra hộp thư.")
        cleaned["user"] = user
        return cleaned

class OTPForm(forms.Form):
    otp_code = forms.CharField(max_length=6, min_length=6)

class Enable2FAConfirmForm(forms.Form):
    otp_code = forms.CharField(max_length=6, min_length=6)

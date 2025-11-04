from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = "accounts"

urlpatterns = [
    # Đăng ký + kích hoạt email
    path("register/", views.register_view, name="register"),
    path("activate/<uidb64>/<token>/", views.activate_email_view, name="activate"),

    # Đăng nhập / đăng xuất / OTP / bật 2FA
    path("login/", views.login_view, name="login"),
    path("otp/", views.otp_verify_view, name="otp_verify"),
    path("logout/", views.logout_view, name="logout"),
    path("enable-2fa/", views.enable_2fa_view, name="enable_2fa"),

    # Ép đổi mật khẩu sau sự cố bảo mật
    path("change-password/", views.change_password_view, name="change_password"),

    # Dashboard người dùng
    path("dashboard/", views.dashboard_view, name="dashboard"),

    # Khu vực staff/admin
    path("staff-area/", views.staff_only_view, name="staff_only"),

    # --- Password reset flow ---
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset_form.html",
            email_template_name="accounts/password_reset_email.txt",
            subject_template_name="accounts/password_reset_subject.txt",
            from_email=None,
            success_url=reverse_lazy("accounts:password_reset_done"),  # <— quan trọng
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),  # <— quan trọng
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]

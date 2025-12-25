from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

from django_ratelimit.decorators import ratelimit

app_name = "accounts"

urlpatterns = [
    # Dang ky tai khoan moi va kich hoat qua email
    path("register/", views.register_view, name="register"),
    path("activate/<uidb64>/<token>/", views.activate_email_view, name="activate"),

    # Quan ly dang nhap, dang xuat va cac chuc nang OTP
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("security/logout-all/", views.logout_all_view, name="logout_all"),
    path("otp/", views.otp_verify_view, name="otp_verify"),
    path("otp/send-email/", views.send_email_otp_view, name="send_email_otp"),
    path("otp/backup/", views.backup_code_verify_view, name="backup_code_verify"),
    
    # Thiet lap bat hoac tat tinh nang bao mat 2 lop
    path("enable-2fa/", views.enable_2fa_view, name="enable_2fa"),
    path("enable-2fa/complete/", views.enable_2fa_complete_view, name="enable_2fa_complete"),
    path("disable-2fa/", views.disable_2fa_view, name="disable_2fa"),

    # Thay doi mat khau nguoi dung
    path("change-password/", views.change_password_view, name="change_password"),

    # Trang bang dieu khien chinh cho nguoi dung
    path("dashboard/", views.dashboard_view, name="dashboard"),

    # Khu vuc danh rieng cho nhan vien noi bo
    path("staff-area/", views.staff_only_view, name="staff_only"),

    # Quy trinh khoi phuc mat khau khi quen (co gioi han request)
    path(
        "password-reset/",
        ratelimit(key='ip', rate='2/m', block=True)
        (auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset_form.html",
            email_template_name="accounts/password_reset_email.txt",
            subject_template_name="accounts/password_reset_subject.txt",
            from_email=None,
            success_url=reverse_lazy("accounts:password_reset_done"),
        )),
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
            success_url=reverse_lazy("accounts:password_reset_complete"),
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
    
    # Quan ly ho so ca nhan va tong quan bao mat
    path("profile/edit/", views.profile_edit_view, name="profile_edit"),
    path('profile/<int:pk>/', views.profile_view, name='profile_view'),
    path("security-dashboard/", views.security_dashboard_view, name="security_dashboard"),
]
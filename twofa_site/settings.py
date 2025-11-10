import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    "nhom8.duckdns.org",
    "47.130.23.25",
    "localhost",
    "127.0.0.1",
]
CSRF_TRUSTED_ORIGINS = [
    'https://nhom8.duckdns.org',
]
INSTALLED_APPS = [
    # ... (giữ nguyên) ...
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "accounts",
    "forum",
]

MIDDLEWARE = [
    # ... (giữ nguyên) ...
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "twofa_site.urls"

TEMPLATES = [
    # ... (giữ nguyên) ...
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "twofa_site.wsgi.application"

DATABASES = {
    # ... (giữ nguyên) ...
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASS"),
        "HOST": os.getenv("DB_HOST", "127.0.0.1"),
        "PORT": os.getenv("DB_PORT", "3306"),
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    }
}

AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    # ... (giữ nguyên) ...
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "vi"
TIME_ZONE = "Asia/Ho_Chi_Minh"
USE_I18N = True
USE_TZ = False

# --- STATIC FILES (SỬA LẠI ĐƯỜNG DẪN) ---
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static_collected"
# SỬA DÒNG DƯỚI ĐÂY:
STATICFILES_DIRS = [ BASE_DIR / "static" ] # Bỏ "twofa_site/"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# ... (giữ nguyên cấu hình email) ...
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/accounts/dashboard/"
LOGOUT_REDIRECT_URL = "/"

SITE_NAME = os.getenv("SITE_NAME", "TwoFA Demo")
SITE_DOMAIN = os.getenv("SITE_DOMAIN", "http://127.0.0.1:8000")

# --- CẤU HÌNH SESSION VÀ BẢO MẬT ---
# Thời hạn session (ví dụ 30 ngày) cho "Tin cậy thiết bị"
SESSION_COOKIE_AGE = 2592000  # 30 * 24 * 60 * 60 = 30 ngày

# Các cài đặt bảo mật (bạn đã có)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

# THÊM CÁC HEADER BẢO MẬT (quan trọng cho production)
SECURE_HSTS_SECONDS = 31536000  # 1 năm
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Cấu hình cho phép người dùng tải file lên (ví dụ: Avatar)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
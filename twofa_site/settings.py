import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False") == "True"

# Danh sach cac ten mien va IP duoc phep truy cap vao server
ALLOWED_HOSTS = [
    "nhom8.duckdns.org",
    "47.130.23.25",
    "localhost",
    "127.0.0.1",
]

# Danh sach cac ten mien tin cay cho bao mat CSRF
CSRF_TRUSTED_ORIGINS = [
    'https://nhom8.duckdns.org',
]

# Khai bao cac ung dung (Apps) duoc cai dat trong du an
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    "django.contrib.humanize", 
    
    "accounts",
    "forum",
    "django_ratelimit", 
]

# Cau hinh cac lop trung gian xu ly request va response
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_ratelimit.middleware.RatelimitMiddleware", 
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "twofa_site.urls"

# Cau hinh giao dien Template HTML
TEMPLATES = [
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

# Cau hinh ket noi co so du lieu MySQL
DATABASES = {
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

# Chi dinh model nguoi dung tuy chinh
AUTH_USER_MODEL = "accounts.User"

# Cac bo kiem tra do manh cua mat khau
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Cau hinh Redis lam bo nho Cache va ho tro Rate Limit
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1", 
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Cau hinh ngon ngu va mui gio
LANGUAGE_CODE = "vi"
TIME_ZONE = "Asia/Ho_Chi_Minh"
USE_I18N = True
USE_TZ = True
USE_L10N = True

# Cau hinh duong dan den cac file tinh (CSS, JS, Images)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static_collected"
STATICFILES_DIRS = [ BASE_DIR / "static" ]


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Cau hinh gui Email qua SMTP Google
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Duong dan mac dinh cho Login va Logout
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/accounts/dashboard/"
LOGOUT_REDIRECT_URL = "/"

# Thong tin chung ve Website
SITE_NAME = os.getenv("SITE_NAME", "TwoFA Demo")
SITE_DOMAIN = os.getenv("SITE_DOMAIN", "http://127.0.0.1:8000")

# Thoi gian song cua session (1 ngay)
SESSION_COOKIE_AGE = 86400 

# Cac cau hinh bao mat SSL/HTTPS cho moi truong Production
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

# Cau hinh bao mat HSTS chan truy cap HTTP thuong
SECURE_HSTS_SECONDS = 31536000 
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Cau hinh noi luu tru file do nguoi dung upload (Media)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Duong dan xu ly khi nguoi dung bi chan do spam (Rate Limit)
RATELIMIT_VIEW = 'accounts.views.ratelimited_error_view'

# Khoa bi mat de ma hoa du lieu OTP trong database
OTP_ENCRYPTION_KEY = os.getenv("OTP_ENCRYPTION_KEY")
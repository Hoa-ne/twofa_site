from django.contrib import admin
from django.urls import path, include
from forum import views as forum_views
from accounts import views as account_views  # Import views của accounts để lấy trang lỗi
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path("quan-tri-vien/", admin.site.urls),

    
    path("admin/", account_views.ratelimited_error_view),

    # Trang chủ
    path("", forum_views.home, name="root_home"),

    # Forum urls
    path("forum/", include(("forum.urls", "forum"), namespace="forum")),

    # Accounts urls (/accounts/... -> login/register/2FA/email/)
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
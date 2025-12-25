from django.contrib import admin
from django.urls import path, include
from forum import views as forum_views
from accounts import views as account_views  # Import views của accounts để lấy trang lỗi
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. TRANG ADMIN THẬT (Đã đổi tên để giấu đi)
    # Bạn có thể đổi 'quan-tri-vien-cap-cao/' thành bất cứ tên gì bạn muốn
    path("quan-tri-vien/", admin.site.urls),

    # 2. TRANG ADMIN GIẢ (Honeypot)
    # Khi hacker/tool quét vào 'admin/', sẽ gặp trang báo lỗi 403 (Cái khiên đỏ)
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
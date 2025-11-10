from django.urls import path
from . import views

app_name = "forum"

urlpatterns = [
    # Trang chủ (liệt kê categories)
    path("", views.home, name="home"),

    # THÊM URL MỚI: Trang chi tiết category (liệt kê threads)
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),

    # Tạo thread mới (giữ nguyên)
    path("new/", views.thread_create, name="thread_create"),

    # Xem chi tiết thread (giữ nguyên)
    path("thread/<int:pk>/", views.thread_detail, name="thread_detail"),

    # THÊM 2 URL MỚI: Sửa và Xóa Post
    path("post/<int:pk>/edit/", views.post_edit_view, name="post_edit"),
    path("post/<int:pk>/delete/", views.post_delete_view, name="post_delete"),
]
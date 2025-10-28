from django.urls import path
from . import views

app_name = "forum"

urlpatterns = [
    # Danh sách thread mới nhất
    path("", views.home, name="home"),

    # Tạo thread mới
    path("new/", views.thread_create, name="thread_create"),

    # Xem chi tiết thread
    path("thread/<int:pk>/", views.thread_detail, name="thread_detail"),
]

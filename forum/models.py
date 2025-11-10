from django.db import models
from django.conf import settings
from django.urls import reverse # Thêm import này

class Category(models.Model):
    # ... (Giữ nguyên) ...
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title
        
    # THÊM HÀM MỚI
    def get_absolute_url(self):
        return reverse("forum:category_detail", kwargs={"slug": self.slug})


class Thread(models.Model):
    # ... (Giữ nguyên) ...
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="threads")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    locked = models.BooleanField(default=False)

    def __str__(self):
        return self.title
        
    # THÊM HÀM MỚI
    def get_absolute_url(self):
        return reverse("forum:thread_detail", kwargs={"pk": self.pk})


class Post(models.Model):
    # ... (Giữ nguyên) ...
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="posts")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.author} on {self.thread}"
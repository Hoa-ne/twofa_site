from django.db import models
from django.conf import settings
from django.urls import reverse 

# Mo hinh danh muc dien dan dung de phan loai cac chu de
class Category(models.Model):
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    # Tra ve ten hien thi cua danh muc
    def __str__(self):
        return self.title
        
    # Lay duong dan tuyet doi den trang chi tiet danh muc
    def get_absolute_url(self):
        return reverse("forum:category_detail", kwargs={"slug": self.slug})


# Mo hinh chu de thao luan nam trong mot danh muc cu the
class Thread(models.Model):
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="threads")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    locked = models.BooleanField(default=False)

    # Tra ve tieu de cua chu de
    def __str__(self):
        return self.title
        
    # Lay duong dan tuyet doi den trang noi dung cua chu de
    def get_absolute_url(self):
        return reverse("forum:thread_detail", kwargs={"pk": self.pk})


# Mo hinh bai dang hoac binh luan cua nguoi dung trong mot chu de
class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="posts")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_posts", blank=True)

    # Tra ve chuoi mo ta ngan gon ve bai dang
    def __str__(self):
        return f"Post by {self.author} on {self.thread}"
        
    # Dem tong so luot thich cua bai dang nay
    def total_likes(self):
        return self.likes.count()
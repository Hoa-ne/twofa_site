import os
import django
import random
from django.utils import timezone
from django.utils.text import slugify

# Thiết lập môi trường
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twofa_site.settings') 
django.setup()

from django.contrib.auth import get_user_model
from forum.models import Category, Thread, Post

User = get_user_model()

# Dữ liệu mẫu
USER_LIST = ['admin', 'mod_te', 'ironman', 'batman', 'thor', 'hulk', 'captain', 'spiderman', 'doctor_strange', 'black_panther']
CAT_DATA = ['Công nghệ', 'Đời sống', 'Game', 'Hỏi đáp', 'Review', 'Chuyện trò', 'Showbiz', 'Thể thao']

TITLES_PREFIX = [
    "Làm sao để", "Hỏi về", "Chia sẻ", "Review", "Cần tư vấn", "Góc thắc mắc:", "Hot:", "[Thảo luận]"
]
TITLES_SUBJECT = [
    "học Python hiệu quả", "mua iPhone 15 hay 16", "build PC 20 triệu", "tán gái tự động", 
    "fix lỗi Django", "ăn gì ở Sài Gòn", "leo rank Liên Minh", "đầu tư Bitcoin", 
    "học tiếng Anh cho người mất gốc", "cài Win 11 không cần TPM"
]

COMMENTS = [
    "Bài viết rất hữu ích.", "Cảm ơn bác đã chia sẻ.", "Hóng cao nhân vào giải đáp.", 
    "Vấn đề này nan giải đấy.", "Google là ra mà bạn ơi.", "Tuyệt vời, +1 like!", 
    "Mình cũng đang gặp lỗi tương tự.", "Chấm hóng.", "Quá hay, bookmark lại ngay."
]

def run():
    print("--- BẮT ĐẦU TẠO DỮ LIỆU ---")
    
    # 1. Xóa dữ liệu cũ
    Post.objects.all().delete()
    Thread.objects.all().delete()
    Category.objects.all().delete()
    print("-> Đã dọn dẹp dữ liệu cũ.")

    # 2. Tạo Users
    users = []
    for name in USER_LIST:
        u, created = User.objects.get_or_create(
            username=name, 
            defaults={'email': f'{name}@example.com'}
        )
        if created:
            u.set_password('123456')
            u.save()
        users.append(u)
    print(f"-> Đã kiểm tra {len(users)} users.")

    # 3. Tạo Categories
    cats = []
    for name in CAT_DATA:
        slug_clean = slugify(name) 
        c, _ = Category.objects.get_or_create(title=name, slug=slug_clean)
        cats.append(c)
    print(f"-> Đã tạo {len(cats)} chuyên mục.")

    # 4. Tạo 60 Threads
    print("-> Đang tạo 60 chủ đề... (Vui lòng đợi)")
    
    for i in range(60):
        # --- ĐOẠN ĐÃ SỬA: BỎ ({i+1}) ĐI ---
        # Chỉ lấy text ngẫu nhiên, không kèm số
        t_prefix = random.choice(TITLES_PREFIX)
        t_subject = random.choice(TITLES_SUBJECT)
        title = f"{t_prefix} {t_subject}" 
        
        # Để tránh trùng lặp 100%, thỉnh thoảng thêm dấu "!" hoặc "?" ngẫu nhiên
        if random.choice([True, False]):
            title += " ?" if "Hỏi" in title or "Làm sao" in title else " !!!"

        author = random.choice(users)
        category = random.choice(cats)
        
        th = Thread.objects.create(
            title=title, 
            category=category, 
            author=author,
            created_at=timezone.now() - timezone.timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
        )
        
        Post.objects.create(
            thread=th,
            author=author,
            content=f"Xin chào mọi người, {title.lower()}. Mong được giúp đỡ! ",
            created_at=th.created_at
        )
        
        # Tạo comment
        num_comments = random.randint(5, 15)
        for _ in range(num_comments):
            Post.objects.create(
                thread=th, 
                author=random.choice(users), 
                content=random.choice(COMMENTS),
                created_at=th.created_at + timezone.timedelta(minutes=random.randint(5, 1000))
            )

    print(f"=== XONG! F5 LẠI TRANG WEB ĐỂ XEM KẾT QUẢ. ===")

if __name__ == '__main__':
    run()
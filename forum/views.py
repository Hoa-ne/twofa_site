from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator # Thêm import này
from django.contrib.auth import get_user_model

from .models import Category, Thread, Post
# Sửa import: Thêm PostForm
from .forms import ThreadCreateForm, PostForm
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST

def home(request):
    """
    SỬA LẠI: Trang chủ diễn đàn giờ là một "dashboard"
    - Lấy danh sách chuyên mục
    - Lấy các chủ đề mới nhất
    - Lấy thống kê
    """
    User = get_user_model() # Lấy model User
    
    categories = Category.objects.all()
    latest_threads = (
        Thread.objects
        .select_related("author", "category")
        .order_by("-created_at")[:15] # Lấy 15 chủ đề mới nhất
    )
    
    # Lấy thống kê
    stats = {
        "total_users": User.objects.count(),
        "total_threads": Thread.objects.count(),
        "total_posts": Post.objects.count(),
    }
    
    context = {
        "categories": categories,
        "latest_threads": latest_threads,
        "stats": stats,
    }
    return render(request, "forum/home.html", context)

# TẠO VIEW MỚI
@login_required
def category_detail(request, slug):
    """
    Trang liệt kê các chủ đề (Thread) trong một Chuyên mục (Category).
    """
    category = get_object_or_404(Category, slug=slug)
    
    # Phân trang cho các chủ đề
    thread_list = Thread.objects.filter(category=category).select_related("author").order_by("-created_at")
    paginator = Paginator(thread_list, 15) # 15 chủ đề/trang
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        "category": category,
        "page_obj": page_obj
    }
    return render(request, "forum/category_detail.html", context)


@login_required
def thread_create(request):
    # ... (Giữ nguyên view thread_create) ...
    if request.method == "POST":
        form = ThreadCreateForm(request.POST)
        if form.is_valid():
            # ... (giữ nguyên logic) ...
            title = form.cleaned_data["title"]
            category = form.cleaned_data["category"]
            content = form.cleaned_data["content"]

            thread = Thread.objects.create(
                title=title,
                category=category,
                author=request.user,
                created_at=timezone.now(),
                locked=False,
            )
            Post.objects.create(
                thread=thread,
                author=request.user,
                content=content,
                created_at=timezone.now(),
            )

            return redirect("forum:thread_detail", pk=thread.id)
    else:
        form = ThreadCreateForm()

    return render(request, "forum/thread_create.html", {"form": form})


def thread_detail(request, pk):
    """
    SỬA LẠI: Thêm Phân trang (Pagination) cho các bài Post.
    """
    thread = get_object_or_404(
        Thread.objects.select_related("author", "category"),
        pk=pk
    )

    # SỬA LẠI: Thêm Paginator
    post_list = (
        Post.objects
        .filter(thread=thread)
        .select_related("author")
        .order_by("created_at") # Sắp xếp theo thời gian tạo
    )
    paginator = Paginator(post_list, 10) # 10 bài/trang
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # Kết thúc sửa

    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Bạn cần đăng nhập để trả lời.")
        # ... (giữ nguyên logic xử lý POST) ...
        if thread.locked:
            return HttpResponseForbidden("Chủ đề này đã bị khóa, không thể trả lời.")

        form = PostForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.thread = thread
            reply.author = request.user
            reply.created_at = timezone.now()
            reply.save()

            # Chuyển đến trang cuối cùng (nơi có bài post mới)
            return redirect(f"{thread.get_absolute_url()}?page={paginator.num_pages}")
    else:
        form = PostForm()

    ctx = {
        "thread": thread,
        "posts": page_obj,
        "page_obj": page_obj,
        "form": form,  # <-- THÊM DÒNG NÀY VÀO
    }
    return render(request, "forum/thread_detail.html", ctx)
# TẠO 2 VIEW MỚI (EDIT/DELETE)

@login_required
def post_edit_view(request, pk):
    """Cho phép user sửa bài post của mình."""
    post = get_object_or_404(Post, pk=pk)
    
    # Chỉ chủ bài post mới được sửa
    if request.user != post.author:
        return HttpResponseForbidden("Bạn không có quyền sửa bài viết này.")
        
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            # Trả về trang chi tiết của thread, tại đúng page của post đó
            return redirect(f"{post.thread.get_absolute_url()}?page={request.GET.get('page', 1)}")
    else:
        form = PostForm(instance=post)
        
    return render(request, "forum/post_form.html", {"form": form, "post": post})

@login_required
def post_delete_view(request, pk):
    """Cho phép user xóa bài post của mình (chỉ xử lý POST)."""
    post = get_object_or_404(Post, pk=pk)
    
    if request.user != post.author:
        return HttpResponseForbidden("Bạn không có quyền xóa bài viết này.")
    
    if request.method == "POST":
        thread = post.thread # Lưu lại thread
        post.delete()
        # Trả về trang thread
        return redirect("forum:thread_detail", pk=thread.id)
    
    # Không nên xóa qua GET, trả về 403
    return HttpResponseForbidden("Chỉ chấp nhận phương thức POST.")
    
@require_POST # Yêu cầu view này chỉ chấp nhận phương thức POST
def toggle_lock_view(request, pk):
    """
    Cho phép Staff/Admin khóa hoặc mở khóa một chủ đề (Thread).
    """
    thread = get_object_or_404(Thread, pk=pk)
    
    # Kiểm tra quyền: Chỉ Staff hoặc Admin mới được làm
    if not request.user.is_staff_role():
        return HttpResponseForbidden("Bạn không có quyền thực hiện hành động này.")
    
    # Thực hiện hành động:
    # Lật ngược trạng thái locked (True -> False, False -> True)
    thread.locked = not thread.locked
    thread.save()
    
    # Quay trở lại đúng trang chủ đề vừa rồi
    return redirect("forum:thread_detail", pk=thread.id)
    
@login_required
@require_POST # Chỉ chấp nhận POST (an toàn)
def toggle_like_view(request, pk):
    """
    Xử lý logic Like/Unlike bằng AJAX.
    """
    post = get_object_or_404(Post, pk=pk)
    
    # Kiểm tra xem user đã like hay chưa
    if post.likes.filter(id=request.user.id).exists():
        # Nếu đã like -> Xóa like (Unlike)
        post.likes.remove(request.user)
        liked = False
    else:
        # Nếu chưa like -> Thêm like
        post.likes.add(request.user)
        liked = True
        
    # Trả về dữ liệu JSON cho JavaScript
    return JsonResponse({
        "liked": liked,
        "total_likes": post.total_likes()
    })
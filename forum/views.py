from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST

from .models import Category, Thread, Post
from .forms import ThreadCreateForm, PostForm

# Lấy User model hiện tại
User = get_user_model()

def home(request):
    """
    Dashboard diễn đàn:
    - Danh sách chuyên mục.
    - Danh sách chủ đề (có hỗ trợ bộ lọc).
    - Thống kê hệ thống.
    """
    # 1. Lấy tiêu chí lọc từ URL (mặc định là 'newest')
    sort_by = request.GET.get('sort', 'newest')
    
    # 2. Khởi tạo QuerySet cơ bản
    threads = Thread.objects.select_related("author", "category")
    
    # 3. Áp dụng sắp xếp dựa trên 'sort_by'
    if sort_by == 'oldest':
        threads = threads.order_by('created_at')       # Cũ nhất trước
    elif sort_by == 'az':
        threads = threads.order_by('title')            # A -> Z
    else:
        threads = threads.order_by('-created_at')      # Mới nhất trước (Mặc định)

    # Lấy 15 bài đầu tiên sau khi đã sắp xếp
    latest_threads = threads[:15]
    
    # 4. Thống kê
    stats = {
        "total_users": User.objects.count(),
        "total_threads": Thread.objects.count(),
        "total_posts": Post.objects.count(),
    }
    
    # Dữ liệu cho Sidebar (Luôn luôn là mới nhất, không ảnh hưởng bởi bộ lọc)
    latest_threads_sidebar = Thread.objects.order_by('-created_at')[:5]
    
    context = {
        "categories": Category.objects.all(),
        "latest_threads": latest_threads,
        "latest_threads_sidebar": latest_threads_sidebar, # Thêm dòng này để fix lỗi sidebar trống
        "stats": stats,
        "current_sort": sort_by, # Quan trọng: để highlight nút đang chọn
    }
    return render(request, "forum/home.html", context)


@login_required
def category_detail(request, slug):
    """Liệt kê các chủ đề trong một chuyên mục."""
    category = get_object_or_404(Category, slug=slug)
    
    thread_list = (
        Thread.objects
        .filter(category=category)
        .select_related("author")
        .order_by("-created_at")
    )
    
    # Phân trang: 15 threads/trang
    paginator = Paginator(thread_list, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        "category": category,
        "page_obj": page_obj
    }
    return render(request, "forum/category_detail.html", context)


@login_required
def thread_create(request):
    """Tạo chủ đề mới (Tạo Thread + Post đầu tiên)."""
    if request.method == "POST":
        form = ThreadCreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            category = form.cleaned_data["category"]
            content = form.cleaned_data["content"]

            # 1. Tạo Thread
            thread = Thread.objects.create(
                title=title,
                category=category,
                author=request.user,
                created_at=timezone.now(),
                locked=False,
            )

            # 2. Tạo Post đầu tiên (nội dung chủ đề)
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
    """Xem chi tiết chủ đề và danh sách bình luận (có phân trang)."""
    thread = get_object_or_404(
        Thread.objects.select_related("author", "category"),
        pk=pk
    )

    # Lấy danh sách post, sắp xếp cũ nhất trước (thứ tự thời gian)
    post_list = (
        Post.objects
        .filter(thread=thread)
        .select_related("author")
        .order_by("created_at")
    )

    # Phân trang: 10 bài/trang
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        # Kiểm tra đăng nhập
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Bạn cần đăng nhập để trả lời.")
        
        # Kiểm tra thread bị khóa
        if thread.locked:
            return HttpResponseForbidden("Chủ đề này đã bị khóa, không thể trả lời.")

        form = PostForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.thread = thread
            reply.author = request.user
            reply.created_at = timezone.now()
            reply.save()

            # Redirect đến trang cuối cùng để thấy comment mới
            return redirect(f"{thread.get_absolute_url()}?page={paginator.num_pages}")
    else:
        form = PostForm()

    context = {
        "thread": thread,
        "page_obj": page_obj, # Dùng chung object page_obj để loop trong template
        "form": form,
    }
    return render(request, "forum/thread_detail.html", context)


@login_required
def post_edit_view(request, pk):
    """Sửa bài viết."""
    post = get_object_or_404(Post, pk=pk)
    
    # Kiểm tra quyền chủ sở hữu
    if request.user != post.author:
        return HttpResponseForbidden("Bạn không có quyền sửa bài viết này.")
        
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            # Quay lại thread, giữ nguyên trang hiện tại nếu có param 'page'
            page = request.GET.get('page', 1)
            return redirect(f"{post.thread.get_absolute_url()}?page={page}")
    else:
        form = PostForm(instance=post)
        
    return render(request, "forum/post_form.html", {"form": form, "post": post})


@login_required
def post_delete_view(request, pk):
    """Xóa bài viết (Chỉ nhận POST để an toàn)."""
    post = get_object_or_404(Post, pk=pk)
    
    if request.user != post.author:
        return HttpResponseForbidden("Bạn không có quyền xóa bài viết này.")
    
    if request.method == "POST":
        thread_id = post.thread.id
        # Lưu ý: Nếu xóa post đầu tiên của thread, logic diễn đàn thường sẽ xóa luôn cả thread.
        # Ở đây ta chỉ xóa post đơn thuần.
        post.delete()
        return redirect("forum:thread_detail", pk=thread_id)
    
    return render(request, "forum/post_confirm_delete.html", {"post": post})


@require_POST
def toggle_lock_view(request, pk):
    """Admin/Staff khóa hoặc mở khóa chủ đề."""
    thread = get_object_or_404(Thread, pk=pk)
    
    # Giả định model User có method is_staff_role() như code cũ của bạn
    # Nếu dùng User mặc định của Django thì sửa thành: if not request.user.is_staff:
    if not getattr(request.user, 'is_staff_role', lambda: request.user.is_staff)():
        return HttpResponseForbidden("Bạn không có quyền thực hiện hành động này.")
    
    thread.locked = not thread.locked
    thread.save()
    
    return redirect("forum:thread_detail", pk=thread.id)


@login_required
@require_POST
def toggle_like_view(request, pk):
    """Like/Unlike bài viết bằng AJAX."""
    post = get_object_or_404(Post, pk=pk)
    
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
        
    return JsonResponse({
        "liked": liked,
        "total_likes": post.total_likes()
    })


def contact_view(request):
    """Trang liên hệ tĩnh."""
    return render(request, "contact.html")
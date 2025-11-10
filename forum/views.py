from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.core.paginator import Paginator # Thêm import này

from .models import Category, Thread, Post
# Sửa import: Thêm PostForm
from .forms import ThreadCreateForm, PostForm


def home(request):
    """
    SỬA LẠI: Trang chủ diễn đàn giờ liệt kê Chuyên mục (Category).
    """
    categories = Category.objects.all()
    return render(request, "forum/home.html", {"categories": categories})

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
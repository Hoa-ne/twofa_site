from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone

from .models import Category, Thread, Post
from .forms import ThreadCreateForm, PostForm


def home(request):
    """
    Trang chủ diễn đàn: liệt kê thread mới nhất.
    """
    threads = (
        Thread.objects
        .select_related("author", "category")
        .order_by("-created_at")[:20]
    )
    return render(request, "forum/home.html", {"threads": threads})


@login_required
def thread_create(request):
    """
    Tạo thread mới:
    - tạo record Thread (title/category/author)
    - tạo luôn Post đầu tiên là nội dung mở đầu
    """
    if request.method == "POST":
        form = ThreadCreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            category = form.cleaned_data["category"]
            content = form.cleaned_data["content"]

            # tạo Thread
            thread = Thread.objects.create(
                title=title,
                category=category,
                author=request.user,
                created_at=timezone.now(),
                locked=False,
            )

            # tạo Post đầu tiên (nội dung mở đầu)
            Post.objects.create(
                thread=thread,
                author=request.user,
                content=content,
                created_at=timezone.now(),
            )

            return redirect("forum:thread_detail", thread_id=thread.id)
    else:
        form = ThreadCreateForm()

    return render(request, "forum/thread_create.html", {"form": form})


def thread_detail(request, pk):
    """
    Xem thread + tất cả post trong đó.
    Đồng thời xử lý form trả lời:
      - chỉ user login mới trả lời
      - nếu thread.locked == True thì chặn trả lời
    """
    thread = get_object_or_404(
        Thread.objects.select_related("author", "category"),
        pk=pk
    )

    posts = (
        Post.objects
        .filter(thread=thread)
        .select_related("author")
        .order_by("created_at")
    )

    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Bạn cần đăng nhập để trả lời.")

        if thread.locked:
            return HttpResponseForbidden("Chủ đề này đã bị khóa, không thể trả lời.")

        form = PostForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.thread = thread
            reply.author = request.user
            reply.created_at = timezone.now()
            reply.save()

            return redirect("forum:thread_detail", pk=thread.id)
    else:
        form = PostForm()

    ctx = {
        "thread": thread,
        "posts": posts,
        "form": form,
    }
    return render(request, "forum/thread_detail.html", ctx)


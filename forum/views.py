from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Category, Thread, Post
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .forms import ThreadCreateForm
from .models import Thread, Post



class ThreadCreateForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ["category", "title"]

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content"]

def home_view(request):
    cats = Category.objects.all().prefetch_related("threads")
    return render(request, "forum/home.html", {"categories": cats})

def thread_detail_view(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    posts = thread.posts.select_related("author").order_by("created_at")

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("accounts:login")

        if thread.locked and not request.user.is_staff_role():
            # không cho thường dân trả lời nếu thread bị khóa
            pass
        else:
            form = PostCreateForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.thread = thread
                post.author = request.user
                post.save()
                return redirect("forum:thread_detail", thread_id=thread.id)
    else:
        form = PostCreateForm()

    return render(request, "forum/thread_detail.html", {
        "thread": thread,
        "posts": posts,
        "form": form,
    })

@login_required
def thread_create_view(request):
    if request.method == "POST":
        tform = ThreadCreateForm(request.POST)
        pform = PostCreateForm(request.POST)
        if tform.is_valid() and pform.is_valid():
            thread = tform.save(commit=False)
            thread.author = request.user
            thread.save()
            post = pform.save(commit=False)
            post.thread = thread
            post.author = request.user
            post.save()
            return redirect("forum:thread_detail", thread_id=thread.id)
    else:
        tform = ThreadCreateForm()
        pform = PostCreateForm()
    return render(request, "forum/thread_create.html", {"tform": tform, "pform": pform})

from django.shortcuts import render, get_object_or_404
from .models import Thread, Post

def home(request):
    # Lấy tối đa 20 thread mới nhất
    threads = (
        Thread.objects
        .select_related("author", "category")
        .order_by("-created_at")[:20]
    )

    return render(request, "forum/home.html", {
        "threads": threads,
    })


def thread_detail(request, pk):
    thread = get_object_or_404(
        Thread.objects.select_related("author", "category"),
        pk=pk,
    )
    posts = (
        Post.objects
        .select_related("author", "thread")
        .filter(thread=thread)
        .order_by("created_at")
    )

    return render(request, "forum/thread_detail.html", {
        "thread": thread,
        "posts": posts,
    })

def thread_create(request):
    """
    Tạo thread mới.
    Yêu cầu user đăng nhập.
    Sau khi tạo xong chuyển về trang chi tiết thread.
    """
    if request.method == "POST":
        form = ThreadCreateForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.created_at = timezone.now()
            thread.locked = False
            thread.save()
            # Optionally: tạo post đầu tiên từ nội dung nào đó? (bạn có thể mở rộng sau)
            return redirect("forum:thread_detail", pk=thread.id)
    else:
        form = ThreadCreateForm()

    return render(request, "forum/thread_create.html", {
        "form": form,
    })


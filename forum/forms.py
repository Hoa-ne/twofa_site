from django import forms
from .models import Thread, Post, Category

class ThreadCreateForm(forms.Form):
    title = forms.CharField(
        label="Tiêu đề",
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "Tiêu đề chủ đề..."
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Chuyên mục",
        widget=forms.Select(attrs={
            "class": "form-input",
        })
    )
    content = forms.CharField(
        label="Nội dung mở đầu",
        widget=forms.Textarea(attrs={
            "class": "form-input",
            "placeholder": "Nhập nội dung mở đầu cho chủ đề...",
            "rows": 5,
        })
    )


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-input",
                "placeholder": "Nhập câu trả lời của bạn...",
                "rows": 4,
            }),
        }
        labels = {
            "content": "Trả lời",
        }

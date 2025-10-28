from django import forms
from .models import Thread

class ThreadCreateForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ["category", "title"]
        widgets = {
            "category": forms.Select(
                attrs={"class": "form-input"}
            ),
            "title": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "Tiêu đề thảo luận"}
            ),
        }
        labels = {
            "category": "Chuyên mục",
            "title": "Tiêu đề",
        }

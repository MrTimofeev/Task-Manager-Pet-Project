from django import forms

from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = [
            "title",
            "content",
            "projects",
            "tasks",
            "tags",
        ]  # Убедись, что tags есть здесь
        widgets = {
            "content": forms.Textarea(attrs={"rows": 10}),
            "projects": forms.SelectMultiple(attrs={"class": "form-select"}),
            "tasks": forms.SelectMultiple(attrs={"class": "form-select"}),
            "tags": forms.SelectMultiple(attrs={"class": "form-select"}),
        }

from django import forms

from .models import Note, NoteLink


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


class NoteLinkForm(forms.ModelForm):
    class Meta:
        model = NoteLink
        fields = ['from_note', 'to_note']
        widgets = {
            'from_note': forms.Select(attrs={'class': 'form-select'}),
            'to_note': forms.Select(attrs={'class': 'form-select'}),
        }
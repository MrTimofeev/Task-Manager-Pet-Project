from datetime import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Comment, Project, Task


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description"]


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "status",
            "due_date",
            "file",
        ]  # Добавляем поле file

    def clean_due_date(self):
        due_date = self.cleaned_data.get("due_date")
        if due_date and due_date < datetime.now().date():
            raise ValidationError("Please select a date in the future.")
        return due_date

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # Получаем текущего пользователя
        super().__init__(*args, **kwargs)
        if user:
            self.fields["project"].queryset = Project.objects.filter(
                user=user
            )  # Фильтруем проекты


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text", "file"]

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import viewsets

from .forms import CommentForm, ProjectForm, RegisterForm, TaskForm
from .models import Comment, Project, Task
from .serializers import ProjectSerializer, TaskSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


@login_required
def project_list(request):
    # Фильтруем проекты по текущему пользователю
    projects = Project.objects.filter(user=request.user)
    return render(request, "projects/list.html", {"projects": projects})


@login_required
def project_detail(request, pk):
    # Получаем проект или возвращаем 404
    project = get_object_or_404(Project, id=pk)

    # Проверяем, что пользователь имеет доступ к проекту
    if project.user != request.user:
        raise PermissionDenied("You don't have permission to view this project.")

    # Получаем все задачи проекта
    tasks = project.tasks.all().order_by("due_date")  # Добавьте сортировку по умолчанию

    # Поиск по названию задачи
    search_query = request.GET.get("search")
    if search_query:
        tasks = tasks.filter(title__icontains=search_query)

    # Фильтрация по статусу
    status = request.GET.get("status")
    if status:
        tasks = tasks.filter(status=status)

    # Фильтрация по due_date
    due_date_before = request.GET.get("due_date_before")
    if due_date_before:
        tasks = tasks.filter(due_date__lte=due_date_before)

    # Сортировка
    ordering = request.GET.get("ordering")
    if ordering:
        tasks = tasks.order_by(ordering)

    # Пагинация (10 задач на страницу)
    paginator = Paginator(tasks, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Передаём данные в шаблон
    return render(
        request,
        "projects/detail.html",
        {
            "project": project,
            "page_obj": page_obj,
            "search_query": search_query,
            "status": status,
            "due_date_before": due_date_before,
            "ordering": ordering,
        },
    )


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, id=pk)
    if (
        task.user != request.user
    ):  # Проверяем, что задача принадлежит текущему пользователю
        raise PermissionDenied("You don't have permission to view this task.")
    return render(request, "tasks/detail.html", {"task": task})


login_required


def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)  # Не сохраняем сразу в базу
            project.user = request.user  # Устанавливаем текущего пользователя
            project.save()  # Теперь сохраняем
            return redirect("project_list")
    else:
        form = ProjectForm()
    return render(request, "projects/create.html", {"form": form})


@login_required
def task_create(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if (
        project.user != request.user
    ):  # Проверяем, что проект принадлежит текущему пользователю
        raise PermissionDenied(
            "You don't have permission to create tasks in this project."
        )
    if request.method == "POST":
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project  # Привязываем задачу к проекту
            task.user = request.user  # Привязываем задачу к текущему пользователю
            task.save()
            messages.success(request, "Task created successfully.")
            return redirect("project_detail", pk=project.id)
    else:
        form = TaskForm()
    return render(request, "tasks/create.html", {"form": form, "project": project})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # Перенаправляем на страницу входа после регистрации
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, id=pk)
    if (
        task.user != request.user
    ):  # Проверяем, что задача принадлежит текущему пользователю
        raise PermissionDenied("You don't have permission to edit this task.")
    if request.method == "POST":
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully.")
            # Перенаправляем на страницу проекта
            return redirect("project_detail", pk=task.project.id)
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/update.html", {"form": form})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, id=pk)
    if (
        task.user != request.user
    ):  # Проверяем, что задача принадлежит текущему пользователю
        raise PermissionDenied("You don't have permission to delete this task.")
    project_id = task.project.id  # Получаем ID проекта
    task.delete()  # Удаляем задачу
    # Перенаправляем на страницу проекта
    return redirect("project_detail", pk=project_id)


@login_required
def add_comment(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.user != request.user:
        raise PermissionDenied("You don't have permission to comment on this task.")
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)  # Добавляем request.FILES
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.user = request.user
            comment.save()
            messages.success(request, "Comment added successfully.")
    return redirect("task_detail", pk=task.id)


@login_required
def protected_file(request, file_path):
    full_path = settings.MEDIA_ROOT / file_path
    if not full_path.exists():
        raise Http404("File not found.")

    # Проверяем, что файл принадлежит текущему пользователю
    if file_path.startswith("task_files/"):
        task = Task.objects.filter(file=file_path).first()
        if task and task.user != request.user:
            raise PermissionDenied("You don't have permission to access this file.")
    elif file_path.startswith("comment_files/"):
        comment = Comment.objects.filter(file=file_path).first()
        if comment and comment.user != request.user:
            raise PermissionDenied("You don't have permission to access this file.")

    return FileResponse(open(full_path, "rb"))

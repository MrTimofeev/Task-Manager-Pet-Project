from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from tasks.models import Project, Task, Comment
from datetime import date

class ModelTests(TestCase):
    def setUp(self):
        # Создаём пользователя и проект для тестов
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.project = Project.objects.create(name="Test Project", user=self.user)

    # Тесты для модели Project
    def test_project_creation(self):
        """Тест создания проекта."""
        project = Project.objects.get(id=self.project.id)
        self.assertEqual(project.name, "Test Project")
        self.assertEqual(project.user, self.user)
        self.assertIsNone(project.description)  # Проверяем, что описание пустое
        self.assertIsNotNone(project.created_at)  # Проверяем, что дата создания установлена
        self.assertIsNotNone(project.updated_at)  # Проверяем, что дата обновления установлена

    def test_project_name_cannot_be_blank(self):
        """Тест: имя проекта не может быть пустым."""
        with self.assertRaises(ValidationError):
            project = Project(name="", user=self.user)
            project.full_clean()  # Вызовет ValidationError, если имя пустое

    def test_project_name_max_length(self):
        """Тест: имя проекта не должно превышать максимальную длину."""
        max_length = Project._meta.get_field('name').max_length
        long_name = "a" * (max_length + 1)
        with self.assertRaises(ValidationError):
            project = Project(name=long_name, user=self.user)
            project.full_clean()  # Вызовет ValidationError, если имя слишком длинное

    def test_project_str_representation(self):
        """Тест: строковое представление проекта."""
        self.assertEqual(str(self.project), "Test Project")

    def test_project_task_count(self):
        """Тест: подсчёт количества задач в проекте."""
        # Создаём несколько задач в проекте
        Task.objects.create(project=self.project, title="Task 1", status="todo", user=self.user)
        Task.objects.create(project=self.project, title="Task 2", status="in_progress", user=self.user)
        self.assertEqual(self.project.tasks.count(), 2)

    def test_project_unique_name_per_user(self):
        """Тест: имя проекта должно быть уникальным для каждого пользователя."""
        with self.assertRaises(Exception):  # Или конкретное исключение, например, IntegrityError
            Project.objects.create(name="Test Project", user=self.user)

    # Тесты для модели Task
    def test_task_creation(self):
        """Тест создания задачи."""
        task = Task.objects.create(
            project=self.project,
            title="Fix bug",
            status="todo",
            due_date=date(2023, 10, 1),  # Используем объект date
            user=self.user
        )
        self.assertEqual(task.title, "Fix bug")
        self.assertEqual(task.project, self.project)
        self.assertEqual(task.user, self.user)
        self.assertEqual(task.status, "todo")
        self.assertEqual(task.due_date, date(2023, 10, 1))  # Сравниваем с объектом date
        self.assertIsNone(task.file.name)  # Проверяем, что файл пустой

    def test_task_status_choices(self):
        """Тест: статус задачи должен быть одним из допустимых значений."""
        valid_statuses = [choice[0] for choice in Task.STATUS_CHOICES]
        task = Task(
            project=self.project,
            title="Test Task",
            status="invalid_status",  # Неправильный статус
            user=self.user
        )
        with self.assertRaises(ValidationError):
            task.full_clean()  # Вызовет ValidationError, если статус недопустим

    def test_task_due_date_can_be_blank(self):
        """Тест: дата выполнения задачи может быть пустой."""
        task = Task.objects.create(
            project=self.project,
            title="Task with no due date",
            status="todo",
            user=self.user
        )
        self.assertIsNone(task.due_date)

    def test_task_str_representation(self):
        """Тест: строковое представление задачи."""
        task = Task.objects.create(
            project=self.project,
            title="Test Task",
            status="todo",
            user=self.user
        )
        self.assertEqual(str(task), "Test Task")

    def test_task_file_upload(self):
        """Тест: загрузка файла в задачу."""
        task = Task.objects.create(
            project=self.project,
            title="Task with file",
            status="todo",
            user=self.user,
            file="task_files/test_file.txt"  # Пример пути к файлу
        )
        self.assertEqual(task.file.name, "task_files/test_file.txt")

    # Тесты для модели Comment
    def test_comment_creation(self):
        """Тест создания комментария."""
        task = Task.objects.create(
            project=self.project,
            title="Test Task",
            status="todo",
            user=self.user
        )
        comment = Comment.objects.create(
            task=task,
            user=self.user,
            text="Test comment"
        )
        self.assertEqual(comment.text, "Test comment")
        self.assertEqual(comment.task, task)
        self.assertEqual(comment.user, self.user)
        self.assertIsNone(comment.file.name)  # Проверяем, что файл пустой

    def test_comment_str_representation(self):
        """Тест: строковое представление комментария."""
        task = Task.objects.create(
            project=self.project,
            title="Test Task",
            status="todo",
            user=self.user
        )
        comment = Comment.objects.create(
            task=task,
            user=self.user,
            text="Test comment"
        )
        self.assertEqual(str(comment), f"Comment by {self.user.username} on {task.title}")

    def test_comment_file_upload(self):
        """Тест: загрузка файла в комментарий."""
        task = Task.objects.create(
            project=self.project,
            title="Test Task",
            status="todo",
            user=self.user
        )
        comment = Comment.objects.create(
            task=task,
            user=self.user,
            text="Test comment",
            file="comment_files/test_file.txt"  # Пример пути к файлу
        )
        self.assertEqual(comment.file.name, "comment_files/test_file.txt")
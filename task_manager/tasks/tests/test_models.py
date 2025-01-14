from django.test import TestCase
from django.contrib.auth.models import User
from tasks.models import Project, Task

class ModelTests(TestCase):
    def setUp(self):
        # Создаём пользователя и проект для тестов
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.project = Project.objects.create(name="Test Project", user=self.user)

    def test_project_creation(self):
        """Тест создания проекта."""
        project = Project.objects.get(id=self.project.id)
        self.assertEqual(project.name, "Test Project")
        self.assertEqual(project.user, self.user)

    def test_task_creation(self):
        """Тест создания задачи."""
        task = Task.objects.create(
            project=self.project,
            title="Fix bug",
            status="todo",
            due_date="2023-10-01",
            user=self.user
        )
        self.assertEqual(task.title, "Fix bug")
        self.assertEqual(task.project, self.project)
        self.assertEqual(task.user, self.user)
        self.assertEqual(task.status, "todo")
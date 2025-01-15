from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from tasks.models import Project, Task

User = get_user_model()


class ViewTests(TestCase):
    def setUp(self):
        # Создаём пользователя и авторизуем его
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")

        # Создаём проект и задачи для тестов
        self.project = Project.objects.create(name="Test Project", user=self.user)
        Task.objects.create(
            project=self.project,
            title="Fix bug",
            status="todo",
            due_date="2023-10-01",
            user=self.user,
        )
        Task.objects.create(
            project=self.project,
            title="Implement feature",
            status="done",
            due_date="2023-10-15",
            user=self.user,
        )

    def test_project_detail_view(self):
        """Тест отображения деталей проекта."""
        response = self.client.get(reverse("project_detail", args=[self.project.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fix bug")
        self.assertContains(response, "Implement feature")

    def test_filter_by_status(self):
        """Тест фильтрации задач по статусу."""
        response = self.client.get(
            reverse("project_detail", args=[self.project.id]), {"status": "done"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Implement feature")
        self.assertNotContains(response, "Fix bug")

    def test_search_by_title(self):
        """Тест поиска задач по названию."""
        response = self.client.get(
            reverse("project_detail", args=[self.project.id]), {"search": "bug"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fix bug")
        self.assertNotContains(response, "Implement feature")

    def test_sort_by_due_date(self):
        """Тест сортировки задач по дате выполнения."""
        response = self.client.get(
            reverse("project_detail", args=[self.project.id]), {"ordering": "due_date"}
        )
        self.assertEqual(response.status_code, 200)
        tasks = response.context["page_obj"]
        self.assertEqual(
            tasks[0].title, "Fix bug"
        )  # Первая задача должна быть "Fix bug"
        self.assertEqual(
            tasks[1].title, "Implement feature"
        )  # Вторая задача должна быть "Implement feature"

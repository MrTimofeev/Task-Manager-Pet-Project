from django.db import models
from tasks.models import Project, Task  # Импортируй модели проектов и задач, если они есть

class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

class Note(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    projects = models.ManyToManyField(Project, related_name='notes', blank=True, verbose_name="Проекты")
    tasks = models.ManyToManyField(Task, related_name='notes', blank=True, verbose_name="Задачи")
    tags = models.ManyToManyField('Tag', related_name='notes', blank=True, verbose_name="Теги")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"
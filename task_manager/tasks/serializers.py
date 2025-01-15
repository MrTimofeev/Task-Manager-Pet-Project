from rest_framework import serializers

from .models import Project, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"  # Включаем все поля модели


class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)  # Вложенные задачи

    class Meta:
        model = Project
        fields = "__all__"  # Включаем все поля модели

from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path(
        "", RedirectView.as_view(url="/projects/")
    ),  # Перенаправление на список проектов
    path("projects/", views.project_list, name="project_list"),
    path("projects/<int:pk>/", views.project_detail, name="project_detail"),
    path("projects/create/", views.project_create, name="project_create"),
    path("tasks/<int:pk>/", views.task_detail, name="task_detail"),
    path(
        "projects/<int:project_id>/tasks/create/", views.task_create, name="task_create"
    ),
    path("accounts/register/", views.register, name="register"),
    path("tasks/<int:pk>/update/", views.task_update, name="task_update"),
    path("tasks/<int:pk>/delete/", views.task_delete, name="task_delete"),
    path("tasks/<int:task_id>/comment/", views.add_comment, name="add_comment"),
    path(
        "tasks/<int:task_id>/update_status/",
        views.update_task_status,
        name="update_task_status",
    ),
]

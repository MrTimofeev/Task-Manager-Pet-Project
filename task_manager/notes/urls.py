from django.urls import path

from . import views

app_name = "notes"

urlpatterns = [
    path("", views.NoteListView.as_view(), name="note_list"),
    path("<int:pk>/", views.NoteDetailView.as_view(), name="note_detail"),
    path("create/", views.NoteCreateView.as_view(), name="note_create"),
    path("<int:pk>/update/", views.NoteUpdateView.as_view(), name="note_update"),
    path("<int:pk>/delete/", views.NoteDeleteView.as_view(), name="note_delete"),
    path("graph/", views.note_graph, name="note_graph"),  # Страница с графом
    path(
        "graph/data/", views.note_graph_data, name="note_graph_data"
    ),  # Данные для графа
    path(
        "link/create/", views.NoteLinkCreateView.as_view(), name="notelink_create"
    ),  # Создание связи
]

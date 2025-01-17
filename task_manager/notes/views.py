import markdown
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import NoteForm, NoteLinkForm
from .models import Note, NoteLink


class NoteListView(ListView):
    model = Note
    template_name = "notes/note_list.html"
    context_object_name = "notes"


class NoteDetailView(DetailView):
    model = Note
    template_name = "notes/note_detail.html"
    context_object_name = "note"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Преобразуй Markdown в HTML
        context["note"].content = markdown.markdown(context["note"].content)
        return context


class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = "notes/note_form.html"  # Убедись, что шаблон существует
    success_url = reverse_lazy("notes:note_list")


class NoteUpdateView(UpdateView):
    model = Note
    template_name = "notes/note_form.html"
    fields = ["title", "content", "projects", "tasks", "tags"]
    success_url = reverse_lazy("notes:note_list")


class NoteDeleteView(DeleteView):
    model = Note
    template_name = "notes/note_confirm_delete.html"
    success_url = reverse_lazy("notes:note_list")


def note_graph_data(request):
    # Получаем все заметки
    notes = Note.objects.all()
    # Получаем все связи между заметками
    links = NoteLink.objects.all()

    # Формируем узлы (nodes)
    nodes = [{"id": note.id, "label": note.title} for note in notes]

    # Формируем связи (edges)
    edges = [{"from": link.from_note.id, "to": link.to_note.id} for link in links]

    # Возвращаем данные в формате JSON
    return JsonResponse({"nodes": nodes, "edges": edges})


def note_graph(request):
    return render(request, "notes/note_graph.html")


class NoteLinkCreateView(CreateView):
    model = NoteLink
    form_class = NoteLinkForm
    template_name = "notes/notelink_form.html"
    success_url = reverse_lazy(
        "notes:note_graph"
    )  # Перенаправляем на страницу с графом после создания связи

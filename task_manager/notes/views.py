import markdown
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import NoteForm
from .models import Note


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

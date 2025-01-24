from django.shortcuts import render, get_object_or_404
from.models import Note
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from .forms import NoteForm
from django.views.generic import CreateView,DetailView, ListView, UpdateView  
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

def add_like_view(request, pk):
    if request.method == 'POST':
        note = get_object_or_404(Note, pk=pk)  
        note.likes += 1
        note.save()
        return HttpResponseRedirect(reverse('notes.detail', args=(pk,)))
    raise Http404

def change_visibility_view(request, pk):
    if request.method == 'POST':
        note = get_object_or_404(Note, pk=pk)  
        note.is_public = not note.is_public
        note.save()
        return HttpResponseRedirect(reverse('notes.detail', args=(pk,)))
    raise Http404

class NotesDeleteView(DeleteView):
    model = Note
    success_url = reverse_lazy('notes.list')
    template_name = 'notes/notes_delete.html'
    login_url = '/admin'
    
class NotesUpdateView(UpdateView):
    model = Note
    success_url = reverse_lazy('notes.list')
    form_class = NoteForm
    login_url = '/admin'

class NotesCreateView(CreateView):
    model = Note
    success_url = reverse_lazy('notes.list')
    form_class = NoteForm
    login_url = '/admin'
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
class NotesListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'notes/notes.html'
    context_object_name = 'notes'
    login_url = '/admin'

    def get_queryset(self):
        return self.request.user.notes.all()

class NotesDetailView(LoginRequiredMixin, DetailView):
    model = Note
    template_name = 'notes/details.html'
    context_object_name = 'note'

class NotesPublicDetailView(DetailView):
    model = Note
    template_name = 'notes/details.html'
    context_object_name = 'note'
    queryset = Note.objects.filter(is_public=True)

class PopularNotesListView(ListView):
    model = Note
    template_name = 'notes/notes.html'
    context_object_name = 'notes'
    queryset = Note.objects.filter(likes__gt=1).order_by('-likes')

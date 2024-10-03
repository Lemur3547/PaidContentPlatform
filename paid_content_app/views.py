from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, DetailView, UpdateView, DeleteView

from paid_content_app.forms import PostForm
from paid_content_app.models import Post


# Create your views here.
class MainPage(TemplateView):
    """Контроллер для главной страницы"""

    def get(self, request, *args, **kwargs):
        return render(request, 'paid_content_app/index.html')


class PostListView(ListView):
    """Контроллер для списка записей"""
    model = Post
    ordering = '-created_at'


class PostCreateView(CreateView):
    """Контроллер для создания записи"""
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('main:posts')


class PostDetailView(DetailView):
    """Контроллер для просмотра записи"""
    model = Post


class PostUpdateView(UpdateView):
    """Контроллер для изменения записи"""
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('main:posts')


class PostDeleteView(DeleteView):
    """Контроллер для удаления записи"""
    model = Post
    success_url = reverse_lazy('main:posts')

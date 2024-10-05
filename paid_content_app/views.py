from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, DetailView, UpdateView, DeleteView

from paid_content_app.forms import PostForm
from paid_content_app.models import Post, PurchasedPost


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

    def form_valid(self, form):
        post = form.save()
        post.user = self.request.user
        post.save()
        return super().form_valid(form)


class PostDetailView(DetailView):
    """Контроллер для просмотра записи"""
    model = Post

    def get_object(self, queryset=None):
        # Ограничение доступа для других пользователей
        post = super().get_object(queryset)
        user = self.request.user
        if post.price == 0 or PurchasedPost.objects.filter(post=post, user=user).exists() or post.user == user:
            return post
        raise PermissionDenied


class PostUpdateView(UpdateView):
    """Контроллер для изменения записи"""
    model = Post
    success_url = reverse_lazy('main:posts')

    def get_form_class(self):
        # Ограничение доступа для других пользователей
        user = self.request.user
        if user == self.object.user:
            return PostForm
        raise PermissionDenied


class PostDeleteView(DeleteView):
    """Контроллер для удаления записи"""
    model = Post
    success_url = reverse_lazy('main:posts')

    def get_object(self, queryset=None):
        # Ограничение доступа для других пользователей
        self.object = super().get_object(queryset)
        user = self.request.user
        if user == self.object.user:
            return self.object
        raise PermissionDenied

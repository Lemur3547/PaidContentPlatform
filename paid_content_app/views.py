import stripe
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, DetailView, UpdateView, DeleteView

from paid_content_app.forms import PostForm
from paid_content_app.models import Post, PurchasedPost
from paid_content_app.services import create_product, create_price, create_session


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
        """Привязка текущего пользователя к создаваемой записи
        Увеличение количества постов у пользователя"""
        post = form.save()
        user = self.request.user
        post.user = user
        user.posts += 1
        post.save()
        user.save()
        return super().form_valid(form)


class PostDetailView(DetailView):
    """Контроллер для просмотра записи. Публикация доступна пользователю, если он уже оплатил эту публикацию,
    или пользователь является владельцем публикации, или публикация бесплатная.
    Иначе возвращается ошибка 403 Forbidden"""

    model = Post

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        user = self.request.user
        purchased_posts = PurchasedPost.objects.filter(post=post, user=user)
        if post.price == 0 or post.user == user:
            return post
        elif purchased_posts.exists():
            for i in purchased_posts:
                response = stripe.checkout.Session.retrieve(i.session_id)
                if response.status == 'complete':
                    return post
        raise PermissionDenied


def pay_redirect(request, pk):
    """Контроллер для формирования сессии для оплаты и переадресации пользователя на страницу оплаты,
    занесения данных об оплате пользователем публикации в базу данных.
    Если пользователь уже ранее оплачивал эту публикацию, или пользователь является владельцем публикации,
    или публикация бесплатная, то идет переадресация на страницу с этой публикацией"""

    post = Post.objects.get(pk=pk)
    purchased_posts = PurchasedPost.objects.filter(post=post, user=request.user)
    if purchased_posts.exists():
        for pur_post in purchased_posts:
            response = stripe.checkout.Session.retrieve(pur_post.session_id)
            if response.status == 'complete':
                return redirect('main:detail_post', pk=post.pk)
    if post.price == 0 or post.user == request.user:
        return redirect('main:detail_post', pk=post.pk)
    product = create_product(post)
    price = create_price(post, product)
    session_id, session_url = create_session(post, price)
    PurchasedPost.objects.create(post=post, user=request.user, session_id=session_id)
    return HttpResponseRedirect(session_url)


class CheckPayment(TemplateView):
    """Контроллер для проверки статуса оплаты и переадресации пользователя на страницу с публикацией.
    Если пользователь уже ранее оплачивал эту публикацию, или пользователь является владельцем публикации,
    или публикация бесплатная, то идет переадресация на страницу с этой публикацией.
    Если пользователь еще не оплачивал публикацию, то идет переадресация на страницу со списком публикаций"""

    def get(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        if post.price == 0 or post.user == request.user:
            return redirect('main:detail_post', pk=post.pk)
        purchased_posts = PurchasedPost.objects.filter(post=post, user=self.request.user)
        if purchased_posts.exists():
            for pur_post in purchased_posts:
                response = stripe.checkout.Session.retrieve(pur_post.session_id)
                if response.status == 'complete':
                    purchased_posts.all().delete()
                    PurchasedPost.objects.create(id=pur_post.id, post=pur_post.post, user=pur_post.user,
                                                 session_id=pur_post.session_id)
                    return redirect('main:detail_post', pk=post.pk)
        return redirect('main:posts')


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
        post = super().get_object(queryset)
        user = self.request.user
        if user == post.user:
            return post
        raise PermissionDenied

    def form_valid(self, form):
        """Уменьшение количества постов у пользователя при удалении"""
        user = self.request.user
        user.posts -= 1
        user.save()
        return super().form_valid(form)


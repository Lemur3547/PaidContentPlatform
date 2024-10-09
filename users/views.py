from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView

from paid_content_app.models import Post
from users.forms import UserRegisterForm
from users.models import User


# Create your views here.
class RegisterView(CreateView):
    """Контроллер для страницы регистрации"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:home')

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect(self.success_url)


@login_required
def home(request):
    return HttpResponseRedirect(reverse('users:user_page', args=[request.user.username]))


class UserPage(DetailView):
    model = User
    template_name = 'users/user_page.html'
    ordering = '-created_at'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        view_user = User.objects.get(username=self.kwargs['pk'])
        context_data['user'] = self.request.user
        context_data['view_user'] = view_user
        context_data['user_posts'] = Post.objects.filter(user=view_user).order_by('-created_at')
        return context_data

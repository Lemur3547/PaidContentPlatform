import random

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DetailView, TemplateView, ListView, UpdateView

from paid_content_app.models import Post
from paid_content_app.services import send_sms
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


# Create your views here.
class RegisterView(CreateView):
    """Контроллер для страницы регистрации"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        """Деактивация пользователя, генерация кода подтверждения и отправка смс на указанный номер."""
        user = form.save()
        user.is_active = False
        user.verification_code = random.randrange(1000, 9999)
        user.save()
        send_sms(user.phone_number, f'Код подтверждения телефона: {user.verification_code}')
        return redirect('users:verification', user.username)


class Verification(TemplateView):
    """Контроллер для страницы подтверждения номера телефона"""

    def get(self, request, *args, **kwargs):
        try:
            # Если текущий пользователь залогинен и не имеет кода доступа, то переадресация на страницу его профиля.
            if not request.user.verification_code:
                return HttpResponseRedirect(reverse('users:user_page', args=[request.user.username]))
        except AttributeError:
            # Если пользователь не залогинен, то у него нет поля verification_code, появляется AttributeError и мы
            # перенаправляем его на страницу верификации
            return render(request, 'paid_content_app/verification.html')

    def post(self, request, *args, **kwargs):
        """Проверка введенного пользователем кода с тем, что записан у него в базе данных.
        Если коды совпадают, то пользователь активируется и автологинется, а код доступа удаляется.
        Если коды не совпадают, или пользователь ввел пустую строку, то идет переадресация на эту же страницу."""
        if request.method == 'POST':
            code = request.POST.get('code')
            if code == '':
                return render(request, 'paid_content_app/verification.html')
            user = get_object_or_404(User, username=request.resolver_match.kwargs['pk'])
            if user.verification_code == int(code):
                user.is_active = True
                user.verification_code = None
                user.save()
                login(request, user)
                return redirect('users:user_page', user.username)
        return render(request, 'paid_content_app/verification.html')


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


class UserList(ListView):
    model = User


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('users:user_page', args=[self.request.user.username])

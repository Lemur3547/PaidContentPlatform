from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, home, UserPage, Verification

app_name = UsersConfig.name

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/redirect/', home, name='home'),
    path('<slug:pk>/verification/', Verification.as_view(), name='verification'),
    path('<slug:pk>/', UserPage.as_view(), name='user_page'),
]

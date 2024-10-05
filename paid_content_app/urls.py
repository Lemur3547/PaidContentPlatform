from django.urls import path

from paid_content_app.apps import PaidContentAppConfig
from paid_content_app.views import PostListView, MainPage, PostCreateView, PostDetailView, PostUpdateView, \
    PostDeleteView, pay_redirect, CheckPayment

app_name = PaidContentAppConfig.name

urlpatterns = [
    path('', MainPage.as_view(), name='index'),
    path('posts/', PostListView.as_view(), name='posts'),
    path('post/create/', PostCreateView.as_view(), name='create_post'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='detail_post'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='edit_post'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='delete_post'),
    path('post/<int:pk>/pay/', pay_redirect, name='pay_post'),
    path('post/<int:pk>/check_payment/', CheckPayment.as_view(), name='check_payment'),
]

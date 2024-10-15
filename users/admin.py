from django.contrib import admin

from users.models import User

# Register your models here.

# Регистрация модели пользователя в админке
admin.site.register(User)

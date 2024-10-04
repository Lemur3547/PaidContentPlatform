from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

alphanumeric = RegexValidator(r'^[0-9a-zA-Z_]*$', 'Имя пользователя должно состоять только из латинских букв, цифр и _')


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True, validators=[alphanumeric], verbose_name='Имя пользователя', primary_key=True)
    email = models.EmailField(max_length=100, verbose_name='Email')

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.username:
            return self.username
        else:
            return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

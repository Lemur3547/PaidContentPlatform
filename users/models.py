from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

NULLABLE = {'null': True, 'blank': True}

alphanumeric = RegexValidator(r'^[0-9a-zA-Z_]*$', 'Имя пользователя должно состоять только из латинских букв, цифр и _')
numeric = RegexValidator(r'^[0-9]*$', 'Номер телефона должен состоять только из цифр')


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True, validators=[alphanumeric], verbose_name='Имя пользователя',
                                primary_key=True)
    email = models.EmailField(max_length=100, verbose_name='Email')
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефона', validators=[numeric])
    nickname = models.CharField(max_length=50, verbose_name='Никнейм', **NULLABLE)
    title = models.CharField(max_length=100, verbose_name='О себе (кратко)', **NULLABLE)
    description = models.TextField(verbose_name='О себе', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', default='users/no_profile.png')
    posts = models.IntegerField(verbose_name='Количество публикаций', default=0)

    first_name = None
    last_name = None

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

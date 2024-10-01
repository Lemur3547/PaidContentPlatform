from django.db import models

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Post(models.Model):
    """Модель записи"""
    name = models.CharField(max_length=255, verbose_name='Название')
    text = models.TextField(verbose_name='Текст записи')
    image = models.ImageField(upload_to='posts/', verbose_name='Изображение', **NULLABLE)
    price = models.IntegerField(verbose_name='Стоимость')
    currency = models.CharField(choices=[('ruble', '₽'), ('dollar', '$'), ('euro', '€')])
    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

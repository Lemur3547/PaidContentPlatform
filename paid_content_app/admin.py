from django.contrib import admin

from paid_content_app.models import Post


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Регистрация модели поста в админке"""
    fields = ('name', 'text', 'image', 'price', 'currency', 'user', )

from django import forms

from paid_content_app.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('user', 'created_at', 'updated_at')

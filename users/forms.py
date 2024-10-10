from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from users.models import User


class UserRegisterForm(UserCreationForm):
    """Форма для регистрации пользователя"""

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'password1', 'password2')

    def clean_phone_number(self):
        cleaned_data = self.cleaned_data['phone_number']
        if not 7 <= len(cleaned_data) <= 15:
            raise ValidationError('Номер телефона должен содержать от 7 до 15 цифр')
        return cleaned_data

from django.test import TestCase, Client
from django.urls import reverse

from users.models import User


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='TestUser')
        self.client.force_login(user=self.user)

    def test_register_GET(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_POST(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'TestUserRegister',
            'phone_number': '89201234567',
            'password1': '1234',
            'password2': '1234'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/TestUserRegister/verification/')
        self.assertEqual(User.objects.all().count(), 2)

    def test_register_phone_error_POST(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'TestUserRegister',
            'phone_number': '123',
            'password1': '1234',
            'password2': '1234'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 1)

    def test_verification_auth_user_GET(self):
        response = self.client.get(reverse('users:verification', args=[self.user.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/TestUser/')

    def test_verification_no_user_GET(self):
        self.client.logout()
        self.client.post(reverse('users:register'), {
            'username': 'NewTestUser',
            'phone_number': '89201234567',
            'password1': '1234',
            'password2': '1234'
        })
        new_user = User.objects.get(username='NewTestUser')
        response = self.client.get(reverse('users:verification', args=[new_user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'paid_content_app/verification.html')

    def test_verification_correct_code_POST(self):
        self.client.logout()
        new_user = User.objects.create(username='NewTestUser', verification_code='1234')
        response = self.client.post(reverse('users:verification', args=[new_user.pk]), {
            'code': '1234'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/NewTestUser/')

    def test_verification_incorrect_code_POST(self):
        self.client.logout()
        new_user = User.objects.create(username='NewTestUser', verification_code='1234')
        response = self.client.post(reverse('users:verification', args=[new_user.pk]), {
            'code': '6457'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'paid_content_app/verification.html')

    def test_verification_empty_code_POST(self):
        self.client.logout()
        new_user = User.objects.create(username='NewTestUser', verification_code='1234')
        response = self.client.post(reverse('users:verification', args=[new_user.pk]), {
            'code': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'paid_content_app/verification.html')

    def test_home_redirect(self):
        response = self.client.get(reverse('users:home'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/TestUser/')

    def test_user_page_view(self):
        response = self.client.get(reverse('users:user_page', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_page.html')

    def test_profile_view(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_form.html')

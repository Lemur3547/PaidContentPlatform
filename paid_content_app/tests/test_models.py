from django.test import TestCase

from paid_content_app.models import Post, PurchasedPost
from users.models import User


class TestModels(TestCase):
    def setUp(self):
        self.post, _ = Post.objects.get_or_create(name='Test', defaults={
            'text': 'test',
            'price': 123,
            'currency': 'rub'
        }
                                                  )
        self.user, _ = User.objects.get_or_create(
            username='testUser',
            defaults={
                'email': 'test@mail.com',
                'phone_number': '89001234567'
            }
        )
        self.pur_post, _ = PurchasedPost.objects.get_or_create(
            post=self.post,
            defaults={
                'user': self.user,
                'session_id': '1234'
            }
        )

    def test_post_str(self):
        self.assertEqual(
            self.post.__str__(),
            'Test'
        )

    def test_pur_post_str(self):
        self.assertEqual(
            self.pur_post.__str__(),
            'Test testUser'
        )

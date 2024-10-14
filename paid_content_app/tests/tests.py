from django.core import management
from django.test import TestCase
from io import StringIO
from paid_content_app.models import Post, PurchasedPost
from paid_content_app.services import create_product, create_price, create_session
from paid_content_app.templatetags.my_tags import media_filter, is_purchased, posts_count
from users.models import User


class TestTemplatetags(TestCase):
    def test_media_filter(self):
        self.assertEqual(
            media_filter('some_url/image.png'),
            '/media/some_url/image.png'
        )

    def test_media_filter_no_path(self):
        self.assertEqual(
            media_filter(path=None),
            '#'
        )

    def test_is_purchased_true(self):
        self.user = User.objects.create(username='TestUser')
        self.an_user = User.objects.create(username='AnotherUser')
        self.post = Post.objects.create(name='TestPost', text='TestText', price=100, currency='rub', user=self.user)

        product = create_product(self.post)
        price = create_price(self.post, product)
        session_id, _ = create_session(self.post, price)
        PurchasedPost.objects.create(post=self.post, user=self.an_user, session_id=session_id)

        self.assertEqual(
            is_purchased(self.post, self.an_user),
            False
        )

    def test_is_purchased_false(self):
        self.user = User.objects.create(username='TestUser')
        self.an_user = User.objects.create(username='AnotherUser')
        self.post = Post.objects.create(name='TestPost', text='TestText', price=100, currency='rub', user=self.user)

        self.assertEqual(
            is_purchased(self.post, self.an_user),
            False
        )

    def test_posts_count(self):
        self.assertEqual(
            posts_count(11),
            'публикаций'
        )
        self.assertEqual(
            posts_count(1),
            'публикация'
        )
        self.assertEqual(
            posts_count(3),
            'публикации'
        )
        self.assertEqual(
            posts_count(5),
            'публикаций'
        )

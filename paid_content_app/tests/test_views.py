from django.test import TestCase, Client
from django.urls import reverse

from paid_content_app.models import Post, PurchasedPost
from paid_content_app.services import create_product, create_price, create_session
from users.models import User


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='TestUser')
        self.an_user = User.objects.create(username='AnotherUser')
        self.post = Post.objects.create(name='TestPost', text='TestText', price=100, currency='rub', user=self.user)
        self.client.force_login(user=self.user)

    def test_main_page(self):
        response = self.client.get(reverse('main:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'paid_content_app/index.html')

    def test_posts_list(self):
        response = self.client.get(reverse('main:posts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'paid_content_app/post_list.html')

    def test_create_post_POST(self):
        response = self.client.post(reverse('main:create_post'), {
            'name': 'TestPost',
            'text': 'TestText',
            'price': 100,
            'currency': 'usd'
        })
        self.assertEqual(response.status_code, 302)

    def test_create_post_GET(self):
        response = self.client.get(reverse('main:create_post'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'paid_content_app/post_form.html')

    def test_detail_post_no_pur_post(self):
        response = self.client.get(reverse('main:detail_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'paid_content_app/post_detail.html')

    def test_detail_post_an_user_with_pur_post(self):
        self.client.force_login(user=self.an_user)
        product = create_product(self.post)
        price = create_price(self.post, product)
        session_id, _ = create_session(self.post, price)
        PurchasedPost.objects.create(post=self.post, user=self.an_user, session_id=session_id)
        response = self.client.get(reverse('main:detail_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 403)

    def test_detail_post_an_user_no_pur_post(self):
        self.client.force_login(user=self.an_user)
        response = self.client.get(reverse('main:detail_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 403)

    def test_edit_post_GET(self):
        response = self.client.get(reverse('main:edit_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'paid_content_app/post_form.html')

    def test_edit_post_another_user_GET(self):
        self.client.force_login(user=self.an_user)
        response = self.client.get(reverse('main:edit_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 403)

    def test_edit_post_POST(self):
        response = self.client.post(reverse('main:edit_post', args=[self.post.pk]), {
            'name': 'TestPostUpd',
            'text': 'TestTextUpd',
            'image': '',
            'price': 100,
            'currency': 'usd',
            'user': self.user.pk,
            'created_at': self.post.created_at,
            'updated_at': self.post.updated_at
        })
        self.assertEqual(response.status_code, 302)

    def test_delete_post_GET(self):
        response = self.client.get(reverse('main:delete_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'paid_content_app/post_confirm_delete.html')

    def test_delete_post_another_user_GET(self):
        self.client.force_login(user=self.an_user)
        response = self.client.get(reverse('main:delete_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 403)

    def test_delete_post_DELETE(self):
        response = self.client.post(reverse('main:delete_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)

    def test_pay_redirect(self):
        response = self.client.get(reverse('main:pay_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)

    def test_pay_redirect_another_user_paid(self):
        self.client.force_login(user=self.an_user)
        product = create_product(self.post)
        price = create_price(self.post, product)
        session_id, _ = create_session(self.post, price)
        PurchasedPost.objects.create(post=self.post, user=self.an_user, session_id=session_id)
        response = self.client.get(reverse('main:pay_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)

    def test_pay_redirect_another_user_not_paid(self):
        self.client.force_login(user=self.an_user)
        response = self.client.get(reverse('main:pay_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PurchasedPost.objects.all().count(), 1)

    def test_check_payment_self_user(self):
        response = self.client.get(reverse('main:check_payment', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/post/{self.post.pk}/')

    def test_check_payment_another_user_paid(self):
        self.client.force_login(user=self.an_user)
        product = create_product(self.post)
        price = create_price(self.post, product)
        session_id, _ = create_session(self.post, price)
        PurchasedPost.objects.create(post=self.post, user=self.an_user, session_id=session_id)
        response = self.client.get(reverse('main:check_payment', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)
        # self.assertEqual(response.url, f'/post/{self.post.pk}/')

    def test_check_payment_another_user_not_paid(self):
        self.client.force_login(user=self.an_user)
        response = self.client.get(reverse('main:check_payment', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/posts/')

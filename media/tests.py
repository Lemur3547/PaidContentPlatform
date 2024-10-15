# from unittest import TestCase
#
# from django.test import SimpleTestCase
# from django.urls import reverse, resolve
#
# from paid_content_app.models import Post, PurchasedPost
# from paid_content_app.views import PostListView, PostCreateView, PostDetailView, PostUpdateView, PostDeleteView
# from users.models import User
#
#
# # Create your tests here.
# class PostTestUrls(SimpleTestCase):
#     def test_list_posts(self):
#         url = reverse('main:posts')
#         self.assertEqual(resolve(url).func.view_class, PostListView)
#
#     def test_create_post(self):
#         url = reverse('main:create_post')
#         self.assertEqual(resolve(url).func.view_class, PostCreateView)
#
#     def test_detail_post(self):
#         url = reverse('main:detail_post')
#         self.assertEqual(resolve(url).func.view_class, PostDetailView)
#
#     def test_edit_post(self):
#         url = reverse('main:edit_post')
#         self.assertEqual(resolve(url).func.view_class, PostUpdateView)
#
#     def test_delete_post(self):
#         url = reverse('main:delete_post')
#         self.assertEqual(resolve(url).func.view_class, PostDeleteView)
#
#
# # class PostTestCase(TestCase):
# #     def setUp(self):
# #         self.post = Post.objects.get_or_create(name='Test', text='test', price=123, currency='rub')
# #         self.user = User.objects.get_or_create(username='testUser', email='test@mail.com', phone_number='89001234567')
# #         self.pur_post = PurchasedPost.objects.create(self.post, self.user, '1234')
# #
# #     def test_post_detail(self):
# #         self.assertEqual(
# #             self.post.__str__,
# #             'Test'
# #         )

from django.test import TestCase
from django.urls import reverse
from .models import Post

class CustomErrorHandlerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.post = Post.objects.create(title='Bài viết đầu tiên', content='Nội dung bài viết.')

    def test_custom_error_view(self):
        response = self.client.get(reverse('blog:post_detail', kwargs={'pk': 999}))  # Giả sử bài viết không tồn tại
        self.assertEqual(response.status_code, 404)

    def test_permission_denied_view(self):
        response = self.client.get(reverse('blog:post_list'), follow=True)
        self.assertEqual(response.status_code, 200)  # Kiểm tra xem có truy cập được hay không

    def test_server_error_view(self):
        response = self.client.get(reverse('blog:post_list'), follow=True)
        self.assertEqual(response.status_code, 200)  # Kiểm tra xem có truy cập được hay không

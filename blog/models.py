from django.db import models
from django.urls import reverse

# Model cho bài viết
class Post(models.Model):
    title = models.CharField(max_length=200)  # Tiêu đề bài viết
    content = models.TextField()  # Nội dung bài viết
    created_at = models.DateTimeField(auto_now_add=True)  # Ngày tạo bài viết tự động

    def __str__(self):
        return self.title

    # Trả về URL chi tiết bài viết
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

# Model cho việc lưu trữ file
class ModelWithFileField(models.Model):
    file_field = models.FileField(upload_to='uploads/')  # Lưu file vào thư mục 'uploads/'

    def __str__(self):
        return self.file_field.name

    # Trả về URL chi tiết file (có thể thay đổi theo yêu cầu)
    def get_absolute_url(self):
        return reverse('file_detail', args=[str(self.id)])

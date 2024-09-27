from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('upload/', views.upload_file, name='upload_file'),
    path('success/', views.success_view, name='success_view'),
]

# Xử lý lỗi 404
handler404 = 'blog.views.custom_404_view'

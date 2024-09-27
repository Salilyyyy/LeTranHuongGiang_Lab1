from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import FormView
from .forms import UploadFileForm, FileFieldForm
from .models import Post, ModelWithFileField

# Trang danh sách bài viết
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

# Chi tiết bài viết
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})

# Tạo bài viết mới
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

# Xóa bài viết
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/delete_post.html', {'post': post})

# Upload file đơn
def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']  # Chỉ truy cập tệp tải lên
            instance = ModelWithFileField(file_field=uploaded_file)
            instance.save()
            return HttpResponseRedirect("/success/url/")
    else:
        form = UploadFileForm()
    return render(request, "blog/upload.html", {"form": form})


class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = "blog/upload.html"
    success_url = "/success/url/"

    def form_valid(self, form):
        file = self.request.FILES["file_field"]
        instance = ModelWithFileField(file_field=file)
        instance.save()
        return super().form_valid(form)

# Trang 404 tùy chỉnh
def custom_404_view(request, exception):
    return render(request, 'blog/404.html', status=404)

# Trang thành công
def success_view(request):
    return render(request, 'blog/success.html')

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

def year_archive(request, year, extra_param=None):
    # Logic xử lý để hiển thị bài viết theo năm
    return HttpResponse(f"Year: {year}, Extra Param: {extra_param}")

def month_archive(request, year, month):
    # Logic xử lý để hiển thị bài viết theo tháng
    return HttpResponse(f"Year: {year}, Month: {month}")

def article_detail(request, year, month, slug):
    # Logic để hiển thị chi tiết bài viết
    return HttpResponse(f"Article: {slug} from {month}/{year}")

def bad_request(request, exception):
    # Xử lý lỗi 400
    return HttpResponse("Bad Request", status=400)

def permission_denied(request, exception):
    # Xử lý lỗi 403
    return HttpResponse("Permission Denied", status=403)

def page_not_found(request, exception):
    # Xử lý lỗi 404
    return HttpResponse("Page Not Found", status=404)

def server_error(request):
    # Xử lý lỗi 500
    return HttpResponse("Server Error", status=500)

def redirect_to_year(request):
    # Redirect đến URL năm cụ thể
    year = 2006
    return HttpResponseRedirect(reverse("news-year-archive", args=(year,)))

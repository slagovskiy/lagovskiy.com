from django.http import HttpResponse
from django.shortcuts import render
from apps.blog.models import Post
from toolbox.capcha import capcha_code, captcha_image


def index(request):
    posts = Post.objects.filter(status=Post.PUBLISHED_STATUS)
    content = {
        'posts': posts
    }
    return render(request, 'index.html', content)


def capcha(request):
    request.session['CAPCHA_CODE'] = capcha_code(4)
    return captcha_image(request.session['CAPCHA_CODE'], 1)


def capcha_check(request, code):
    data = '0'
    if request.session['CAPCHA_CODE'] == str(code).upper():
        return HttpResponse('1', content_type="application/javascript")
    else:
        return HttpResponse('0', content_type="application/javascript")

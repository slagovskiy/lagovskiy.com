from django.http import HttpResponse
from django.shortcuts import render

from .blog.models import Post
from .photo.models import Photo
from .toolbox.captcha import captcha_code, captcha_image


def index(request):
    posts = Post.objects.filter(status=Post.PUBLISHED_STATUS).order_by('-published')[0:5]
    photos = Photo.objects.filter(status=Photo.PUBLISHED_STATUS).order_by('-published')[0:4]
    content = {
        'posts': posts,
        'photos': photos
    }
    return render(request, 'index.html', content)


def captcha(request):
    request.session['CAPTCHA_CODE'] = captcha_code(4)
    return captcha_image(request.session['CAPTCHA_CODE'], 1)


def captcha_check(request, code):
    data = '0'
    if request.session['CAPTCHA_CODE'] == str(code).upper():
        return HttpResponse('1', content_type="application/javascript")
    else:
        return HttpResponse('0', content_type="application/javascript")

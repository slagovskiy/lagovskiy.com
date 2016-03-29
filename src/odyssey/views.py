from django.shortcuts import render
from apps.blog.models import Post


def index(request):
    posts = Post.objects.filter(status=Post.PUBLISHED_STATUS)
    content = {
        'posts': posts
    }
    return render(request, 'index.html', content)

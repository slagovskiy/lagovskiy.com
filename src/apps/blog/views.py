from django.shortcuts import render
from .models import Post, Category, Tag


def blog_view(request):
    posts = Post.objects.all().filter(status=Post.PUBLISHED_STATUS)
    content = {
        'posts': posts
    }
    return render(request, 'index.html', content)

def blog_post_view(request, slug=''):
    post = Post.objects.filter(slug=slug, status=Post.PUBLISHED_STATUS).first()
    content = {
        'post': post
    }
    return render(request, 'blog/post_view.html', content)

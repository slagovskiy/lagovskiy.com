from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Post, Category, Tag, Comment
from .settings import PAGE_SIZE


def blog_view(request):
    page = int(request.GET.get('page', 1))
    posts = Post.objects.all().filter(status=Post.PUBLISHED_STATUS)
    paginator = Paginator(posts, PAGE_SIZE)
    if page <= 0:
        page = 1
        if page > paginator.num_pages:
            page = paginator.num_pages

    content = {
        'posts': paginator.page(page)
    }
    return render(request, 'blog/index.html', content)


def blog_post_view(request, slug=''):
    post = Post.objects.filter(slug=slug, status=Post.PUBLISHED_STATUS).first()
    content = {
        'post': post
    }
    return render(request, 'blog/post_view.html', content)


def blog_post_by_tag(request, slug=''):
    page = int(request.GET.get('page', 1))
    tag = Tag.objects.filter(slug=slug).first()
    posts = tag.post_set.filter(status=Post.PUBLISHED_STATUS)
    paginator = Paginator(posts, PAGE_SIZE)
    if page <= 0:
        page = 1
        if page > paginator.num_pages:
            page = paginator.num_pages

    content = {
        'posts': paginator.page(page),
        'active_tag': tag
    }
    return render(request, 'blog/index.html', content)


def blog_post_by_category(request, slug=''):
    page = int(request.GET.get('page', 1))
    category = Category.objects.filter(slug=slug).first()
    posts = category.post_set.filter(status=Post.PUBLISHED_STATUS)
    paginator = Paginator(posts, PAGE_SIZE)
    if page <= 0:
        page = 1
        if page > paginator.num_pages:
            page = paginator.num_pages

    content = {
        'posts': paginator.page(page),
        'active_category': category
    }
    return render(request, 'blog/index.html', content)

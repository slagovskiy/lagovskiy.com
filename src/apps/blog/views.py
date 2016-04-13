from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from toolbox.utils import get_ip
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


def blog_comment(request, id):
    comment = Comment.objects.get(id=id)
    content = {
        'comment': comment
    }
    return render(request, 'blog/comment_view.html', content)


def blog_comment_save(request):
    data = None
    if request.POST:
        parent = int(request.POST.get('parent', 0))
        post = int(request.POST.get('post', 0))
        message = str(request.POST.get('comment-message', ''))
        username = str(request.POST.get('comment-username', 'guest'))
        email = str(request.POST.get('comment-email', ''))
        captcha = str(request.POST.get('comment-captcha', ''))
        agent = request.META.get('HTTP_USER_AGENT', '')
        ip = get_ip(request)
        if request.session['CAPTCHA_CODE'] == str(captcha).upper():
            post = Post.objects.get(id=post)
            if post:
                parent_comment = None
                if parent > 0:
                    parent_comment = Comment.objects.get(id=parent)
                comment = Comment()
                comment.post = post
                comment.content = message
                comment.username = username
                comment.email = email
                comment.agent = agent
                comment.ip = ip
                comment.save()
                if parent == 0:
                    comment.path = str(comment.id)
                else:
                    comment.path = parent_comment.path + '-' + str(comment.id)
                comment.save()
                return HttpResponse('ok:' + str(comment.id))
            else:
                return HttpResponse('unknown post:0')
        else:
            return HttpResponse('wrong captcha:0')
    else:
        return HttpResponse('wrong method:0')

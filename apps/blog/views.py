# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.models import User, AnonymousUser
from django.db.models import Q

from datetime import date
from datetime import timedelta
from datetime import datetime

import logging

from apps.blog.models import *
from apps.blog.settings import *

def custom_proc(request):
    return {
        'app_title': 'Blog',
        'link_app': 'blog',
        'user': request.user,
        'ip_address': request.META['REMOTE_ADDR'],
        'ajax': request.GET.get('ajax', 0)
    }

def index(request):
    message = ''
    posts = []
    page = int(request.GET.get('page', 1))
    try:
        posts = Post.objects.all().filter(status=Post.PUBLISHED_STATUS).order_by('-sticked', '-published')
        paginator = Paginator(posts, PAGE_SIZE)
        if page<=0:
            page = 1
        if page>paginator.num_pages:
            page = paginator.num_pages
    except:
        logging.exception('Error get posts list')
    t = loader.get_template('blog/default.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'posts': paginator.page(page),
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def postby_tag(request, tag):
    message = ''
    posts = []
    tags = None
    page = int(request.GET.get('page', 1))
    try:
        tags = Tag.objects.get(slug=tag)
        posts = Post.objects.all().filter(status=Post.PUBLISHED_STATUS, tags=tags).order_by('-sticked', '-published')
        paginator = Paginator(posts, PAGE_SIZE)
        if page<=0:
            page = 1
        if page>paginator.num_pages:
            page = paginator.num_pages
    except:
        logging.exception('Error get posts list')
    t = loader.get_template('blog/default.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'posts': paginator.page(page),
            'group': 'tag',
            'group_id': tags.id,
            'filter': tag,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))


def postby_category(request, category):
    message = ''
    posts = []
    categories = None
    page = int(request.GET.get('page', 1))
    try:
        categories = Category.objects.get(slug=category)
        posts = Post.objects.all().filter(status=Post.PUBLISHED_STATUS, categories=categories).order_by('-sticked', '-published')
        paginator = Paginator(posts, PAGE_SIZE)
        if page<=0:
            page = 1
        if page>paginator.num_pages:
            page = paginator.num_pages
    except:
        logging.exception('Error get posts list')
    t = loader.get_template('blog/default.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'posts': paginator.page(page),
            'group': 'category',
            'group_id': categories.id,
            'filter': category,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def post_view(request, slug):
    message = ''
    formmessage = ''
    post = None
    try:
        post = Post.objects.all().filter(slug=slug)[0]
        formmessage = request.GET.get('formmessage', '')
    except:
        logging.exception('Error get post')
    if post:
        if post.status==Post.HIDDEN_STATUS or post.status==Post.PUBLISHED_STATUS:
            t = loader.get_template('blog/post_view.html')
            c = RequestContext(
                request,
                {
                    'message': message,
                    'post': post,
                    'comments': request.session.get('sended_comments', []),
                    'formmessage': formmessage,
                    'custom_title': post.title,
                    'meta_keywords': post.keywords,
                    'meta_description': post.description,
                    },
                processors=[custom_proc],)
            return HttpResponse(t.render(c))
        else:
            HttpResponseRedirect('/blog/')
    return HttpResponseRedirect('/blog/')

def comment_count(request, post_id):
    message = ''
    count = 0
    post = None
    try:
        post = Post.objects.get(id=post_id)
        if post:
            count = post.comment_count()
    except:
        logging.exception('Error get comments count')
    t = loader.get_template('ajax.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'data': count,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def comment_save(request, id):
    report = ''
    user = None
    root = None
    try:
        post = Post.objects.get(id=id)
        if post:
            _reply = ''
            _name = ''
            _email = ''
            _message = ''
            _subscribe = ''
            ajax = '0'
            _id = '-1'
            _reply = request.POST.get('comment_reply', '0')
            _name = request.POST.get('comment_name', 'guest')
            _email = request.POST.get('comment_email', '')
            _message = request.POST.get('comment_content', '')
            _subscribe = request.POST.get('comment_subscribe', False)
            ajax = request.POST.get('ajax', '0')
            if _reply!='0':
                root = Comment.objects.get(id=int(_reply))
            if Comment.objects.all().filter(
                    published__range=(datetime.today()-timedelta(minutes=COMMENT_MINUTES_LIMIT), datetime.today()),
                    post=post,
                    agent=request.META['HTTP_USER_AGENT'],
                    ip=request.META['REMOTE_ADDR']
            ).count()==0:
                comment = Comment.objects.create(
                    post = post,
                    user = user,
                    name = _name,
                    email = _email,
                    content = _message,
                    agent = request.META['HTTP_USER_AGENT'],
                    ip = request.META['REMOTE_ADDR'],
                    allowed = not post.comments_moderated,
                    )
                comment.save()
                #try:
                #    sended_comments = []
                #    if request.session.get('sended_comments', [])!=None:
                #        sended_comments = request.session.get('sended_comments', [])
                #    sended_comments.append(comment.id)
                #    request.session['sended_comments']=sended_comments
                #except:
                #    logging.exception('Error add comment to session var')
                if (_subscribe=='True') & (_email!=''):
                    if SubscribePost.objects.all().filter(post=post, email=_email).count()==0:
                        subscribe = SubscribePost.objects.create(
                            post = post,
                            email = _email,
                            active = not post.comments_moderated
                        )
                        subscribe.save()
                    #else:
                    #    subscribe = SubscribePost.objects.all().filter(post=post, email=_email)[0]
                    #    subscribe.active = True
                    #    subscribe.save()
                if not post.comments_moderated:
                    for subscribe in SubscribePost.objects.all().filter(post=post, active=True):
                        mq = CommentMessageQueue.objects.create(
                            subscribe = subscribe,
                            comment = comment,
                            active = True
                        )
                        mq.save()
                comment_id = comment.id
                if root:
                    comment.parent = root
                    comment.save()
                return HttpResponseRedirect('/blog/view/'+post.slug+'/#comment'+str(comment.id))
            else:
                return HttpResponseRedirect('/blog/view/'+post.slug+'/'+u'?formmessage=You can not add more than one comment for ' + str(COMMENT_MINUTES_LIMIT) + ' minute.#add_comment')
    except:
        report = u'Error adding comment'
        logging.exception(u'Error adding comment')
    t = loader.get_template('ajax.html')
    c = RequestContext(
        request,
        {
            'message': report,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

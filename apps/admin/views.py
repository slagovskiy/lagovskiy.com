from unicodedata import category
from django.core.context_processors import request
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.models import User, AnonymousUser
from django.db.models import Q
from django.db.models.aggregates import Max
from django.contrib.auth import authenticate, login, logout

from datetime import date
from datetime import timedelta
from datetime import datetime

import logging
import random
from apps.blog.admin import CategoryAdmin

from apps.blog.models import *
from apps.blog.settings import *

from utils import *

from apps.blog.models import Category

def custom_proc(request):
    return {
        'app_title': 'Admin',
        'link_app': 'admin',
        #'link_category': '',
        #'link_tag': '',
        'user': request.user,
        'ip_address': request.META['REMOTE_ADDR'],
        'ajax': request.GET.get('ajax', 0)
    }

# utils

def check_access(user, access):
    try:
        if not getattr(user.get_profile(), access)():
            return False
        else:
            return True
    except:
        return False


def random_str(size):
    """
    return random string
    """
    str = 'qwertyuiopasdfghjklzxcvbnm'
    return ''.join([random.choice(str) for i in range(size)])




def index(request):
    message = ''
    t = loader.get_template('admin/default.html')
    c = RequestContext(
        request,
        {
            'message': message,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

# login / logout

def login_action(request):
    message = ''
    t = loader.get_template('admin/login.html')
    c = RequestContext(
        request,
        {
            'message': message,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def login_check(request):
    _login = request.POST.get('txtLogin', '')
    _password = request.POST.get('txtPassword', '')
    logging.warning(_login)
    logging.warning(_password)
    page = request.POST.get('return', '/')
    if page == None:
        page = '/'
    user = authenticate(username=_login, password=_password)
    logging.warning(user)
    if user is not None:
        if user.is_active:
            login(request, user)
    return HttpResponseRedirect(page)

def logout_action(request):
    page = request.META.get('HTTP_REFERER')
    if page == None:
        page = '/'
    logout(request)
    return HttpResponseRedirect(page)

def ad(request):
    message = ''
    t = loader.get_template('admin/access_denied.html')
    c = RequestContext(
        request,
        {
            'message': message,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

# blog

## blog: category

def blog_category(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    t = loader.get_template('admin/blog/category.html')
    c = RequestContext(
        request,
        {
            'message': message,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_category_getall(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    categories = []
    try:
        categories = Category.objects.all()
    except:
        logging.error('Error get categories list')
    t = loader.get_template('admin/blog/category_getall.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'categories': categories,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_category_getlist(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    categories = []
    try:
        categories = Category.objects.all().filter(deleted=False)
    except:
        logging.error('Error get categories list')
    t = loader.get_template('admin/blog/category_getall.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'categories': categories,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_category_edit(request, id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    category = None
    try:
        if id!=0:
            category = Category.objects.get(id=id)
    except:
        logging.error('Error get category item')
    t = loader.get_template('admin/blog/category_edit.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'category': category,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_category_save(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    try:
        category = None
        tmp_id = request.POST.get('_id', 0)
        tmp_name = request.POST.get('_name', '')
        tmp_slug = request.POST.get('_slug', '')
        tmp_sort = request.POST.get('_sort', 100)
        tmp_deleted = request.POST.get('_deleted', False)
        logging.warning(tmp_id)
        if tmp_id!='':
            category = Category.objects.get(id=tmp_id)
            category.slug = tmp_slug
            category.name = tmp_name
            category.sort = tmp_sort
            if tmp_deleted=="True":
                category.deleted = True
            else:
                category.deleted = False
            category.save()
        else:
            category = Category.objects.create(
                slug = tmp_slug,
                name = tmp_name,
                sort = tmp_sort,
            )
            if tmp_deleted=="True":
                category.deleted = True
            else:
                category.deleted = False
            category.save()
    except:
        logging.exception('Error save or add category')
    return  HttpResponseRedirect('/admin/blog/category/')

def blog_category_moveup(request, id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    try:
        categories = Category.objects.all()
        category = None
        category_prev = None
        for category in categories:
            if category.id==int(id):
                if category_prev:
                    tmp = category.sort
                    category.sort = category_prev.sort
                    category_prev.sort = tmp
                    category.save()
                    category_prev.save()
            category_prev = category
    except:
        logging.exception('Error move up category')
    return  HttpResponseRedirect('/admin/blog/category/')

def blog_category_movedown(request, id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    try:
        categories = Category.objects.all()
        category = None
        category_prev = None
        for category in reversed(categories):
            if category.id==int(id):
                if category_prev:
                    tmp = category.sort
                    category.sort = category_prev.sort
                    category_prev.sort = tmp
                    category.save()
                    category_prev.save()
            category_prev = category
    except:
        logging.exception('Error move up category')
    return  HttpResponseRedirect('/admin/blog/category/')


## blog: tag

def blog_tag(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    t = loader.get_template('admin/blog/tag.html')
    c = RequestContext(
        request,
        {
            'message': message,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_tag_getall(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    tags = []
    try:
        tags = Tag.objects.all()
    except:
        logging.error('Error get tags list')
    t = loader.get_template('admin/blog/tag_getall.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'tags': tags,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_tag_getlist(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    tags = []
    try:
        tags = Tag.objects.all().filter(deleted=False)
    except:
        logging.error('Error get tags list')
    t = loader.get_template('admin/blog/tag_getall.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'tags': tags,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_tag_edit(request, id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    tag = None
    try:
        if id!=0:
            tag = Tag.objects.get(id=id)
    except:
        logging.error('Error get tag item')
    t = loader.get_template('admin/blog/tag_edit.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'tag': tag,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_tag_save(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    try:
        tag = None
        tmp_id = request.POST.get('_id', 0)
        tmp_name = request.POST.get('_name', '')
        tmp_slug = request.POST.get('_slug', '')
        tmp_sort = request.POST.get('_sort', 100)
        tmp_deleted = request.POST.get('_deleted', False)
        logging.warning(tmp_id)
        if tmp_id!='':
            tag = Tag.objects.get(id=tmp_id)
            tag.slug = tmp_slug
            tag.name = tmp_name
            tag.sort = tmp_sort
            if tmp_deleted=="True":
                tag.deleted = True
            else:
                tag.deleted = False
            tag.save()
        else:
            tag = Tag.objects.create(
                slug = tmp_slug,
                name = tmp_name,
                sort = tmp_sort,
            )
            if tmp_deleted=="True":
                tag.deleted = True
            else:
                tag.deleted = False
            tag.save()
    except:
        logging.exception('Error save or add tag')
    return  HttpResponseRedirect('/admin/blog/tag/')

def blog_tag_moveup(request, id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    try:
        tags = Tag.objects.all()
        tag = None
        tag_prev = None
        for tag in tags:
            if tag.id==int(id):
                if tag_prev:
                    tmp = tag.sort
                    tag.sort = tag_prev.sort
                    tag_prev.sort = tmp
                    tag.save()
                    tag_prev.save()
            tag_prev = tag
    except:
        logging.exception('Error move up tag')
    return  HttpResponseRedirect('/admin/blog/tag/')

def blog_tag_movedown(request, id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    try:
        tags = Tag.objects.all()
        tag = None
        tag_prev = None
        for tag in reversed(tags):
            if tag.id==int(id):
                if tag_prev:
                    tmp = tag.sort
                    tag.sort = tag_prev.sort
                    tag_prev.sort = tmp
                    tag.save()
                    tag_prev.save()
            tag_prev = tag
    except:
        logging.exception('Error move up tag')
    return  HttpResponseRedirect('/admin/blog/tag/')

## post

def blog_post(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    t = loader.get_template('admin/blog/post.html')
    c = RequestContext(
        request,
        {
            'message': message,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_post_getall(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    posts = []
    try:
        posts = Post.objects.all()
    except:
        logging.error('Error get post list')
    t = loader.get_template('admin/blog/post_getall.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'posts': posts,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_post_edit(request, id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    post = None
    users = []
    try:
        users = User.objects.all()
        if id=='0':
            post = Post.objects.create(
                title = "New post",
                slug = random_str(16),
                author = request.user
            )
            post.save()
        else:
            post = Post.objects.get(id=id)
    except:
        logging.error('Error get post item')
    t = loader.get_template('admin/blog/post_edit.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'post': post,
            'users': users,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_post_save(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    post = None
    try:
        _id = request.POST.get('_id', '0')
        _slug = request.POST.get('_slug', '')
        _title = request.POST.get('_title', '')
        _author = request.POST.get('_author', '')
        _revision = request.POST.get('_revision', 0)
        if _revision=='': _revision = 0
        _desription = request.POST.get('_description', '')
        _keywords = request.POST.get('_keywords', '')
        _status = request.POST.get('_status', '1')
        _sticked = request.POST.get('_sticked', False)
        _comments_enabled = request.POST.get('_comments_enabled', False)
        _comments_moderated = request.POST.get('_comments_moderated', True)
        _do_ping = request.POST.get('_do_ping')
        _published = request.POST.get('_published', '')
        _published_time = request.POST.get('_published_time', '')
        _categories = request.POST.getlist('_categories', [])
        _tags = request.POST.getlist('_tags', [])

        post = Post.objects.get(id=_id)
        post.slug = _slug
        post.title = _title
        post.author = User.objects.get(id=_author)
        post.published_revision = _revision
        post.desription = _desription
        post.keywords = _keywords
        post.status = _status
        post.sticked = _sticked
        post.comments_enabled = _comments_enabled
        post.comments_moderated = _comments_moderated
        post.do_ping = _do_ping
        if (_published!='') and (_published_time!=''):
            post.published = datetime.strptime(_published + ' ' + _published_time, '%Y/%m/%d %H:%M')
        post.save()

        post.categories.clear()
        for _category in _categories:
            post.categories.add(Category.objects.get(id=_category))

        post.tags.clear()
        for _tag in _tags:
            post.tags.add(Tag.objects.get(id=_tag))
        post.save()

    except:
        logging.error('Error save post item')
    return HttpResponseRedirect('/admin/blog/post/')

## revision

def blog_revision_getlist(request, post_id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    revisions = []
    post = None
    try:
        post = Post.objects.get(id=post_id)
        revisions = PostRevision.objects.all().filter(post=post).order_by('created')
    except:
        logging.error('Error get revisions list')
    t = loader.get_template('admin/blog/revision_getall.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'revisions': revisions,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_revision_getexcerpt(request, id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    revision = None
    try:
        revision = PostRevision.objects.get(id=id)
    except:
        logging.error('Error get revisions list')
    t = loader.get_template('admin/blog/data.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'data': revision.excerpt,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_revision_getcontent(request, id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    revision = None
    try:
        revision = PostRevision.objects.get(id=id)
    except:
        logging.error('Error get revisions list')
    t = loader.get_template('admin/blog/data.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'data': revision.content,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_revision_create(request, post_id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    post = None
    revision = None
    try:
        post = Post.objects.get(id=post_id)
        revision = PostRevision.objects.all().filter(post=post, revision=-1)
        if len(revision)==0:
            revision = PostRevision.objects.create(
                post = post,
                revision = -1,
            )
            revision.save()
        else:
            revision = revision[0]
            revision.excerpt = ''
            revision.content = ''
            revision.created = datetime.now()
            revision.save()
    except:
        logging.error('Error create revision')
    t = loader.get_template('admin/blog/data.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'data': revision.id,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))


def blog_revision_save(request, post_id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    post = None
    revision = None
    try:
        post = Post.objects.get(id=post_id)
        revision = PostRevision.objects.all().filter(post=post, revision=-1)
        if len(revision)==0:
            revision = PostRevision.objects.create(
                post = post,
                revision = -1,
            )
            revision.save()
        else:
            revision = revision[0]
        revision.excerpt = request.POST.get('excerpt', '')
        revision.content = request.POST.get('content', '')
        revision.created = datetime.now()
        revision.save()
    except:
        logging.error('Error save revision')
    t = loader.get_template('admin/blog/data.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'data': revision.id,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_revision_fix(request, id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    post = None
    revision = None
    revision_old = None
    try:
        revision_old = PostRevision.objects.get(id=id)
        max = PostRevision.objects.filter(post = revision_old.post).exclude(revision=-1).aggregate(Max('revision'))['revision__max']
        if not max:
            max = 0
        revision = PostRevision.objects.create(
            post = revision_old.post,
            excerpt = request.POST.get('excerpt', ''),
            content = request.POST.get('content', ''),
            revision = max + 1,
            created = datetime.now()
        )
        revision.save()
    except:
        logging.error('Error fix revision')
    t = loader.get_template('admin/blog/data.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'data': revision.id,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_revision_preview(request, id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    revision = None
    try:
        revision = PostRevision.objects.get(id=id)
    except:
        logging.error('Error get revisions list')
    t = loader.get_template('admin/blog/revision_preview.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'revision': revision,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

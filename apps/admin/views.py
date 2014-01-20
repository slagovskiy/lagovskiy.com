from unicodedata import category
from django.core.context_processors import request
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.models import User, AnonymousUser
from django.db.models import Q
from django.db.models.aggregates import Max, Count, Avg
from django.contrib.auth import authenticate, login, logout

from datetime import date
from datetime import timedelta
from datetime import datetime

import logging
import random
from apps.blog.admin import CategoryAdmin

from apps.blog.models import *

from apps.robot.models import *

from apps.banner.models import *

from apps.statistic.models import *

from urllib2 import unquote

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
    page = request.POST.get('return', '/')
    if page == None:
        page = '/'
    user = authenticate(username=_login, password=_password)
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
        logging.exception('Error get categories list')
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
        logging.exception('Error get categories list')
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
        logging.exception('Error get category item')
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
        if (tmp_name==''): tmp_name = 'qwerty'
        if (tmp_slug==''): tmp_slug = 'qwerty'
        if (tmp_sort==''): tmp_sort = 1000
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
        logging.exception('Error get tags list')
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
        logging.exception('Error get tags list')
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
        logging.exception('Error get tag item')
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
        if (tmp_slug==''): tmp_slug = 'qwerty'
        if (tmp_name==''): tmp_name = 'qwerty'
        if (tmp_sort==''): tmp_sort = 1000
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
        posts = Post.objects.all().order_by('status', '-published', 'title')
    except:
        logging.exception('Error get post list')
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
                author = request.user,
                do_ping = True
            )
            post.save()
        else:
            post = Post.objects.get(id=id)
    except:
        logging.exception('Error get post item')
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
        _description = request.POST.get('_description', '')
        _keywords = request.POST.get('_keywords', '')
        _status = request.POST.get('_status', '1')
        _sticked = request.POST.get('_sticked', False)
        _comments_enabled = request.POST.get('_comments_enabled', False)
        _comments_moderated = request.POST.get('_comments_moderated', False)
        _do_ping = request.POST.get('_do_ping', False)
        _published = request.POST.get('_published', '')
        _published_time = request.POST.get('_published_time', '00:00')
        _categories = request.POST.getlist('_categories', [])
        _tags = request.POST.getlist('_tags', [])

        logging.warning('====================================')
        logging.warning(request.POST.get('_id', '0'))
        logging.warning(request.POST.get('_slug', ''))
        logging.warning(request.POST.get('_title', ''))
        logging.warning(request.POST.get('_author', ''))
        logging.warning(request.POST.get('_revision', 0))
        logging.warning(request.POST.get('_description', ''))
        logging.warning(request.POST.get('_keywords', ''))
        logging.warning(request.POST.get('_status', '1'))
        logging.warning(request.POST.get('_sticked', False))
        logging.warning(request.POST.get('_comments_enabled', False))
        logging.warning(request.POST.get('_comments_moderated', False))
        logging.warning(request.POST.get('_do_ping', False))
        logging.warning(request.POST.get('_published', ''))
        logging.warning(request.POST.get('_published_time', '00:00'))
        logging.warning(request.POST.getlist('_categories', []))
        logging.warning(request.POST.getlist('_tags', []))
        logging.warning('====================================')

        post = Post.objects.get(id=_id)
        post.slug = _slug
        post.title = _title
        post.author = User.objects.get(id=_author)
        post.published_revision = _revision
        post.description = _description
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
        logging.exception('Error save post item')
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
        logging.exception('Error get revisions list')
    t = loader.get_template('admin/blog/revision_getall.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'revisions': revisions,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_revision_getteaser(request, id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    revision = None
    try:
        revision = PostRevision.objects.get(id=id)
    except:
        logging.exception('Error get revisions list')
    t = loader.get_template('admin/blog/data.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'data': revision.teaser,
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
        logging.exception('Error get revisions list')
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
            revision.teaser = ''
            revision.content = ''
            revision.created = datetime.now()
            revision.save()
    except:
        logging.exception('Error create revision')
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
        revision.teaser = request.POST.get('teaser', '')
        revision.content = request.POST.get('content', '')
        revision.created = datetime.now()
        revision.save()
    except:
        logging.exception('Error save revision')
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
            teaser = request.POST.get('teaser', ''),
            content = request.POST.get('content', ''),
            revision = max + 1,
            created = datetime.now()
        )
        revision.save()
    except:
        logging.exception('Error fix revision')
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
        logging.exception('Error get revisions list')
    t = loader.get_template('admin/blog/revision_preview.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'revision': revision,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

## comment

def blog_comment_getlist(request, id):
    if not check_access(request.user, 'canCommentDelete'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    post = None
    backlink = ''
    try:
        post = Post.objects.get(id=id)
    except:
        logging.exception('Error get comments list')
    t = loader.get_template('admin/blog/comment_getall.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'post': post,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_comment_edit(request, id):
    if not check_access(request.user, 'canCommentDelete'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    comment = None
    try:
        comment = Comment.objects.get(id=id)
    except:
        logging.exception('Error get comment for edit')
    t = loader.get_template('admin/blog/comment_edit.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'comment': comment,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_comment_save(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    try:
        tmp_id = request.POST.get('_id', 0)
        tmp_name = request.POST.get('_name', '')
        tmp_content = request.POST.get('_content', '')
        comment = Comment.objects.get(id=tmp_id)
        comment.name = tmp_name
        comment.content = tmp_content
        comment.save()
    except:
        logging.exception('Error save comment')
    return  HttpResponseRedirect('/admin/blog/post/')

def blog_comment_delete(request, id):
    if not check_access(request.user, 'canCommentDelete'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    comment = None
    backlink = ''
    try:
        backlink = request.GET.get('backlink', '')
        comment = Comment.objects.get(id=id)
        comment.deleted = True
        comment.save()
    except:
        logging.exception('Error get comment for delete')
    if backlink!='':
        return HttpResponseRedirect(backlink)
    else:
        return HttpResponseRedirect('/')

def blog_comment_restore(request, id):
    if not check_access(request.user, 'canCommentDelete'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    comment = None
    backlink = ''
    try:
        backlink = request.GET.get('backlink', '')
        comment = Comment.objects.get(id=id)
        comment.deleted = False
        comment.save()
    except:
        logging.exception('Error get comment for restore')
    if backlink!='':
        return HttpResponseRedirect(backlink)
    else:
        return HttpResponseRedirect('/')

def blog_comment_allow(request, id):
    if not check_access(request.user, 'canCommentDelete'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    comment = None
    user = None
    backlink = ''
    subscribe = []
    try:
        comment = Comment.objects.get(id=id)
        backlink = request.GET.get('backlink', '')
        if comment:
            comment.allowed = True
            comment.save()
            post = comment.post
            post.do_ping = True
            post.save()
            subscribe = SubscribePost.objects.all().filter(post=comment.post, email=comment.email)
            if subscribe.count()>0:
                tmp = subscribe[0]
                tmp.active = True
                tmp.save()
            for subscribe in SubscribePost.objects.all().filter(post=comment.post, active=True):
                mq = CommentMessageQueue.objects.create(
                    subscribe = subscribe,
                    comment = comment,
                    active = True
                )
                mq.save()
    except:
        report = u'Error allowing comment'
        logging.exception(u'Error allowing comment')
    if backlink!='':
        return HttpResponseRedirect(backlink)
    else:
        return HttpResponseRedirect('/')

## images

def blog_postimage_list(request, post_id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    post = None
    images = []
    try:
        post = Post.objects.get(id=post_id)
        images = PostImage.objects.filter(post=post)
    except:
        logging.exception(u'Error get PostImage list')
    t = loader.get_template('admin/blog/postimage_list.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'images': images,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_postimage_edit(request, post_id, id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    image = None
    try:
        if id!=0:
            image = PostImage.objects.get(id=id)
    except:
        logging.exception('Error get postimage item')
    t = loader.get_template('admin/blog/postimage_edit.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'image': image,
            'post_id': post_id,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_postimage_insert(request, id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    image = None
    try:
        if id!=0:
            image = PostImage.objects.get(id=id)
    except:
        logging.exception('Error get postimage item')
    t = loader.get_template('admin/blog/postimage_insert.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'image': image,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_postimage_delete(request, id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    image = None
    tmp_post_id = 0
    try:
        if id!=0:
            image = PostImage.objects.get(id=id)
            tmp_post_id = image.post_id
            image.delete()
    except:
        logging.exception('Error delete postimage item')
    return  HttpResponseRedirect('/admin/blog/post/edit/' + str(tmp_post_id) + '/')

def blog_postimage_save(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    tmp_post_id = 0
    tmp_id = 0
    image = None
    post = None
    try:
        tmp_id = request.POST.get('_id', 0)
        tmp_post_id = request.POST.get('_post_id', 0)
        tmp_description = request.POST.get('_description', '')
        tmp_img_xxs = request.POST.get('_img_xxs', '')
        tmp_img_xs = request.POST.get('_img_xs', '')
        tmp_img_s = request.POST.get('_img_s', '')
        tmp_img_m = request.POST.get('_img_m', '')
        tmp_img_l = request.POST.get('_img_l', '')
        tmp_img_xl = request.POST.get('_img_xl', '')
        tmp_img_xxl = request.POST.get('_img_xxl', '')
        tmp_img_xxxl = request.POST.get('_img_xxxl', '')
        tmp_img_orig = request.POST.get('_img_orig', '')
        if tmp_post_id!='':
            post = Post.objects.get(id=tmp_post_id)
        if tmp_id!='':
            image = PostImage.objects.get(id=tmp_id)
            image.description = tmp_description
            image.img_xxs = tmp_img_xxs
            image.img_xs = tmp_img_xs
            image.img_s = tmp_img_s
            image.img_m = tmp_img_m
            image.img_l = tmp_img_l
            image.img_xl = tmp_img_xl
            image.img_xxl = tmp_img_xxl
            image.img_xxxl = tmp_img_xxxl
            image.img_orig = tmp_img_orig
            image.post = post
            image.save()
        else:
            image = PostImage.objects.create(
                description = tmp_description,
                img_xxs = tmp_img_xxs,
                img_xs = tmp_img_xs,
                img_s = tmp_img_s,
                img_m = tmp_img_m,
                img_l = tmp_img_l,
                img_xl = tmp_img_xl,
                img_xxl = tmp_img_xxl,
                img_xxxl = tmp_img_xxxl,
                img_orig = tmp_img_orig,
                post = post,
                )
            image.save()
    except:
        logging.exception('Error save or add postimage')
    return  HttpResponseRedirect('/admin/blog/post/edit/' + tmp_post_id + '/')


## robot: pingserver

def robot_pingserver(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    t = loader.get_template('admin/robot/pingserver.html')
    c = RequestContext(
        request,
        {
            'message': message,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def robot_pingserver_getall(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    pingservers = []
    try:
        pingservers = PingServer.objects.all()
    except:
        logging.exception('Error get pingserver list')
    t = loader.get_template('admin/robot/pingserver_getall.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'pingservers': pingservers,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def robot_pingserver_edit(request, id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    pingserver = None
    try:
        if id!=0:
            pingserver = PingServer.objects.get(id=id)
    except:
        logging.exception('Error get ping server item')
    t = loader.get_template('admin/robot/pingserver_edit.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'pingserver': pingserver,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def robot_pingserver_save(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    try:
        pingserver = None
        tmp_id = request.POST.get('_id', 0)
        tmp_address = request.POST.get('_address', '')
        tmp_type = request.POST.get('_type', '')
        tmp_deleted = request.POST.get('_deleted', False)
        if (tmp_address==''): tmp_address = 'http://none'
        if (tmp_type==''): tmp_type = 1
        if tmp_id!='':
            pingserver = PingServer.objects.get(id=tmp_id)
            pingserver.address = tmp_address
            pingserver.type = tmp_type
            if tmp_deleted=="True":
                pingserver.deleted = True
            else:
                pingserver.deleted = False
            pingserver.save()
        else:
            pingserver = PingServer.objects.create(
                address = tmp_address,
                type = tmp_type,
            )
            if tmp_deleted=="True":
                pingserver.deleted = True
            else:
                pingserver.deleted = False
            pingserver.save()
    except:
        logging.exception('Error save or add pingserver')
    return  HttpResponseRedirect('/admin/robot/pingserver/')


## robot: pingresult

def robot_pingresult(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    t = loader.get_template('admin/robot/pingresult.html')
    c = RequestContext(
        request,
        {
            'message': message,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def robot_pingresult_date(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    items = []
    try:
        items = PingResult.objects.values('date').annotate(name=Avg('date'))
    except:
        logging.exception('Error get pingserver list')
    t = loader.get_template('admin/robot/pingresult_getby.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'items': items,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def robot_pingresult_post(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    items = []
    try:
        items = PingResult.objects.values('post__title', 'post').annotate(name=Avg('post'))
    except:
        logging.exception('Error get pingserver list')
    t = loader.get_template('admin/robot/pingresult_getby.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'items': items,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def robot_pingresult_subpost(request, id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    items = []
    try:
        items = PingResult.objects.filter(post_id=id).values('date').annotate(name=Avg('date'))
    except:
        logging.exception('Error get pingserver list')
    t = loader.get_template('admin/robot/pingresult_getby.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'items': items,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def robot_pingresult_subdate(request, d_y, d_m, d_d):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    items = []
    filter_date = date(int(d_y), int(d_m), int(d_d))
    try:
        items = PingResult.objects.filter(date=filter_date).values('post__title', 'post').annotate(name=Avg('post'))
    except:
        logging.exception('Error get pingserver list')
    t = loader.get_template('admin/robot/pingresult_getby.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'items': items,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def robot_pingresult_subdatepost(request, d_y, d_m, d_d, id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    items = []
    filter_date = date(int(d_y), int(d_m), int(d_d))
    try:
        items = PingResult.objects.filter(date=filter_date, post=id)
    except:
        logging.exception('Error get pingserver list')
    t = loader.get_template('admin/robot/pingresult_getall.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'items': items,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def robot_pingresult_subpostdate(request, id, d_y, d_m, d_d):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    items = []
    filter_date = date(int(d_y), int(d_m), int(d_d))
    try:
        items = PingResult.objects.filter(date=filter_date, post=id)
    except:
        logging.exception('Error get pingserver list')
    t = loader.get_template('admin/robot/pingresult_getall.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'items': items,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))



## banners

def banner_index(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    t = loader.get_template('admin/banner/default.html')
    c = RequestContext(
        request,
        {
            'message': message,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def banner_getall(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    banners = []
    try:
        banners = Banner.objects.all()
    except:
        logging.exception('Error get categories list')
    t = loader.get_template('admin/banner/banner_getall.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'banners': banners,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def banner_getlist(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    banners = []
    try:
        banners = Banner.objects.all().filter(deleted=False)
    except:
        logging.exception('Error get banners list')
    t = loader.get_template('admin/banner/banner_getall.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'banners': banners,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def banner_edit(request, id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    banner = None
    try:
        if id!=0:
            banner = Banner.objects.get(id=id)
    except:
        logging.exception('Error get category item')
    t = loader.get_template('admin/banner/banner_edit.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'banner': banner,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def banner_save(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    try:
        banner = None
        tmp_id = request.POST.get('_id', 0)
        tmp_name = request.POST.get('_name', '')
        tmp_slug = request.POST.get('_slug', '')
        tmp_code = request.POST.get('_code', '')
        tmp_sort = request.POST.get('_sort', 100)
        tmp_deleted = request.POST.get('_deleted', False)
        tmp_hidden = request.POST.get('_hidden', False)
        logging.warning(tmp_deleted)
        logging.warning(tmp_hidden)
        if (tmp_name==''): tmp_name = 'qwerty'
        if (tmp_slug==''): tmp_slug = 'qwerty'
        if (tmp_sort==''): tmp_sort = 1000
        if tmp_id!='':
            banner = Banner.objects.get(id=tmp_id)
            banner.slug = tmp_slug
            banner.name = tmp_name
            banner.code = tmp_code
            banner.sort = tmp_sort
            if tmp_deleted=="True":
                banner.deleted = True
            else:
                banner.deleted = False
            if tmp_hidden=="True":
                banner.hidden = True
            else:
                banner.hidden = False
            banner.save()
        else:
            banner = Banner.objects.create(
                slug = tmp_slug,
                name = tmp_name,
                code = tmp_code,
                sort = tmp_sort,
                )
            if tmp_deleted=="True":
                banner.deleted = True
            else:
                banner.deleted = False
            if tmp_hidden=="True":
                banner.hidden = True
            else:
                banner.hidden = False
            banner.save()
    except:
        logging.exception('Error save or add banner')
    return  HttpResponseRedirect('/admin/banner/')

def banner_moveup(request, id):
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

def banner_movedown(request, id):
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

def visitors_by_point(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    visitors = []
    try:
        visitors = Visitor.objects.all().filter(point=unquote(request.GET.get('p', '')), day=unquote(request.GET.get('d', ''))).order_by('date')
    except:
        logging.exception('Error get visitors list')
    t = loader.get_template('admin/statistic/visitors_getall.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'visitors': visitors,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def visitors_dates(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    visitors = []
    try:
        visitors = Visitor.objects.all()\
            .filter(point=unquote(request.GET.get('p', '')))\
            .values_list('day').order_by('-day').distinct()
    except:
        logging.exception('Error get visitors list')
    t = loader.get_template('admin/statistic/visitors_dates.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'visitors': visitors,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_subscribe_getlist(request, id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    post = None
    subscribs = []
    try:
        post = Post.objects.get(id=id)
        subscribs = SubscribePost.objects.all().filter(post=post)
    except:
        logging.exception('Error get subscribe list')
    t = loader.get_template('admin/blog/subscribe_getall.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'subscribs': subscribs,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_subscribe_edit(request, id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    subscribe = None
    try:
        if id!=0:
            subscribe = SubscribePost.objects.get(id=id)
    except:
        logging.exception('Error get subscribe item')
    t = loader.get_template('admin/blog/subscribe_edit.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'subscribe': subscribe,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_subscribe_save(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    try:
        subscribe = None
        tmp_id = request.POST.get('_id', 0)
        tmp_email = request.POST.get('_email', '')
        tmp_active = request.POST.get('_active', False)
        if tmp_id!='':
            subscribe = SubscribePost.objects.get(id=tmp_id)
            subscribe.email = tmp_email
            if tmp_active=="True":
                subscribe.active = True
            else:
                subscribe.active = False
            subscribe.save()
        else:
            subscribe = SubscribePost.objects.create(
                email = tmp_email
                )
            if tmp_active=="True":
                subscribe.active = True
            else:
                subscribe.active = False
            subscribe.save()
    except:
        logging.exception('Error save or add subscribe')
    return  HttpResponseRedirect('/admin/blog/post/')

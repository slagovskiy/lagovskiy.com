from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from apps.blog.models import *
from apps.robot.models import *
from apps.statistic.models import *
from apps.blog.models import Category
from apps.admin.utils import *
from apps.admin.views import custom_proc


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


def blog_post_edit(request, post_id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    post = None
    users = []
    try:
        users = User.objects.all()
        if post_id == '0':
            post = Post.objects.create(
                title="New post",
                slug=random_str(16),
                author=request.user,
                do_ping=True
            )
            post.save()
        else:
            post = Post.objects.get(id=post_id)
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
    try:
        _id = request.POST.get('_id', '0')
        _slug = request.POST.get('_slug', '')
        _title = request.POST.get('_title', '')
        _author = request.POST.get('_author', '')
        _revision = request.POST.get('_revision', 0)
        if _revision == '':
            _revision = 0
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
        if _published != '' and _published_time != '':
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
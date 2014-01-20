from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from apps.blog.models import *
from apps.robot.models import *
from apps.statistic.models import *
from apps.admin.utils import *
from apps.admin.views import custom_proc


def blog_revision_getlist(request, post_id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    revisions = []
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


def blog_revision_getteaser(request, revision_id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    revision = None
    try:
        revision = PostRevision.objects.get(id=revision_id)
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


def blog_revision_getcontent(request, revision_id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    revision = None
    try:
        revision = PostRevision.objects.get(id=revision_id)
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
    revision = None
    try:
        post = Post.objects.get(id=post_id)
        revision = PostRevision.objects.all().filter(post=post, revision=-1)
        if len(revision) == 0:
            revision = PostRevision.objects.create(
                post=post,
                revision=-1,
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
    revision = None
    try:
        post = Post.objects.get(id=post_id)
        revision = PostRevision.objects.all().filter(post=post, revision=-1)
        if len(revision) == 0:
            revision = PostRevision.objects.create(
                post=post,
                revision=-1,
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


def blog_revision_fix(request, revision_id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    revision = None
    try:
        revision_old = PostRevision.objects.get(id=revision_id)
        max_revision = \
            PostRevision.objects.filter(post=revision_old.post).exclude(revision=-1).aggregate(Max('revision'))[
                'revision__max']
        if not max_revision:
            max_revision = 0
        revision = PostRevision.objects.create(
            post=revision_old.post,
            teaser=request.POST.get('teaser', ''),
            content=request.POST.get('content', ''),
            revision=max_revision + 1,
            created=datetime.now()
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


def blog_revision_preview(request, revision_id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    revision = None
    try:
        revision = PostRevision.objects.get(id=revision_id)
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
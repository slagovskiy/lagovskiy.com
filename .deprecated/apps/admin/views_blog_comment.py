from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from apps.blog.models import *
from apps.robot.models import *
from apps.statistic.models import *
from apps.admin.utils import *
from apps.admin.views import custom_proc


def blog_comment_getlist(request, post_id):
    if not check_access(request.user, 'canCommentDelete'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    post = None
    try:
        post = Post.objects.get(id=post_id)
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


def blog_comment_edit(request, comment_id):
    if not check_access(request.user, 'canCommentDelete'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    comment = None
    try:
        comment = Comment.objects.get(id=comment_id)
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
    return HttpResponseRedirect('/admin/blog/post/')


def blog_comment_delete(request, comment_id):
    if not check_access(request.user, 'canCommentDelete'):
        return HttpResponseRedirect('/admin/ad/')
    backlink = ''
    try:
        backlink = request.GET.get('backlink', '')
        comment = Comment.objects.get(id=comment_id)
        comment.deleted = True
        comment.save()
    except:
        logging.exception('Error get comment for delete')
    if backlink != '':
        return HttpResponseRedirect(backlink)
    else:
        return HttpResponseRedirect('/')


def blog_comment_restore(request, comment_id):
    if not check_access(request.user, 'canCommentDelete'):
        return HttpResponseRedirect('/admin/ad/')
    backlink = ''
    try:
        backlink = request.GET.get('backlink', '')
        comment = Comment.objects.get(id=comment_id)
        comment.deleted = False
        comment.save()
    except:
        logging.exception('Error get comment for restore')
    if backlink != '':
        return HttpResponseRedirect(backlink)
    else:
        return HttpResponseRedirect('/')


def blog_comment_allow(request, comment_id):
    if not check_access(request.user, 'canCommentDelete'):
        return HttpResponseRedirect('/admin/ad/')
    backlink = ''
    try:
        comment = Comment.objects.get(id=comment_id)
        backlink = request.GET.get('backlink', '')
        if comment:
            comment.allowed = True
            comment.save()
            post = comment.post
            post.do_ping = True
            post.save()
            subscribe = SubscribePost.objects.all().filter(post=comment.post, email=comment.email)
            if subscribe.count() > 0:
                tmp = subscribe[0]
                tmp.active = True
                tmp.save()
            for subscribe in SubscribePost.objects.all().filter(post=comment.post, active=True):
                mq = CommentMessageQueue.objects.create(
                    subscribe=subscribe,
                    comment=comment,
                    active=True
                )
                mq.save()
    except:
        logging.exception(u'Error allowing comment')
    if backlink != '':
        return HttpResponseRedirect(backlink)
    else:
        return HttpResponseRedirect('/')
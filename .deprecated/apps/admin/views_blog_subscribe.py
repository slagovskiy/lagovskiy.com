from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from apps.blog.models import *
from apps.robot.models import *
from apps.statistic.models import *
from apps.admin.utils import *
from apps.admin.views import custom_proc


def blog_subscribe_getlist(request, post_id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    subscribs = []
    try:
        post = Post.objects.get(id=post_id)
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


def blog_subscribe_edit(request, subscribe_id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    subscribe = None
    try:
        if id != 0:
            subscribe = SubscribePost.objects.get(id=subscribe_id)
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
    try:
        tmp_id = request.POST.get('_id', 0)
        tmp_email = request.POST.get('_email', '')
        tmp_active = request.POST.get('_active', False)
        if tmp_id != '':
            subscribe = SubscribePost.objects.get(id=tmp_id)
            subscribe.email = tmp_email
            if tmp_active == "True":
                subscribe.active = True
            else:
                subscribe.active = False
            subscribe.save()
        else:
            subscribe = SubscribePost.objects.create(
                email=tmp_email
            )
            if tmp_active == "True":
                subscribe.active = True
            else:
                subscribe.active = False
            subscribe.save()
    except:
        logging.exception('Error save or add subscribe')
    return  HttpResponseRedirect('/admin/blog/post/')
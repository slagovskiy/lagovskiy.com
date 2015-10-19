from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from apps.blog.models import *
from apps.robot.models import *
from apps.statistic.models import *
from apps.admin.utils import *
from apps.admin.views import custom_proc


def blog_postimage_list(request, post_id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
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


def blog_postimage_edit(request, post_id, image_id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    image = None
    try:
        if id != 0:
            image = PostImage.objects.get(id=image_id)
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


def blog_postimage_insert(request, image_id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    image = None
    try:
        if image_id != 0:
            image = PostImage.objects.get(id=image_id)
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


def blog_postimage_delete(request, image_id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    tmp_post_id = 0
    try:
        if image_id != 0:
            image = PostImage.objects.get(id=image_id)
            tmp_post_id = image.post_id
            image.delete()
    except:
        logging.exception('Error delete postimage item')
    return HttpResponseRedirect('/admin/blog/post/edit/' + str(tmp_post_id) + '/')


def blog_postimage_save(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    tmp_post_id = 0
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
        if tmp_post_id != '':
            post = Post.objects.get(id=tmp_post_id)
        if tmp_id != '':
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
                description=tmp_description,
                img_xxs=tmp_img_xxs,
                img_xs=tmp_img_xs,
                img_s=tmp_img_s,
                img_m=tmp_img_m,
                img_l=tmp_img_l,
                img_xl=tmp_img_xl,
                img_xxl=tmp_img_xxl,
                img_xxxl=tmp_img_xxxl,
                img_orig=tmp_img_orig,
                post=post,
            )
            image.save()
    except:
        logging.exception('Error save or add postimage')
    return HttpResponseRedirect('/admin/blog/post/edit/' + tmp_post_id + '/')
import json
import os
from uuid import uuid4
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.dateparse import parse_datetime
from apps.userext.utils import admin_check
from apps.blog.models import Tag, Category, Post
from apps.links.models import MyLink
from apps.media.models import Folder, File
from apps.media.utils import create_icon
from odyssey.settings import UPLOAD_DIR
from toolbox.imghdr import what
from toolbox.models import Global


@login_required()
@user_passes_test(admin_check)
def index(request):
    content = {
    }
    return render(request, 'admin/index.html', content)


def login_action(request):
    if request.POST:
        username = request.POST.get('txtUsername', '')
        password = request.POST.get('txtPassword', '')
        next = request.GET.get('next', '/')
        user = authenticate(
            username=username,
            password=password
        )
        if user is not None:
            if user.is_active:
                login(request, user)
        return redirect(next)
    return render(request, 'admin/login.html')


@login_required()
def logout_action(request):
    logout(request)
    return redirect('/')


@login_required()
@user_passes_test(admin_check)
def global_view(request, id=None):
    data = None
    if request.POST:
        # save data
        id = int(request.POST.get('id', 0))
        slug = str(request.POST.get('txtSlug', ''))
        value = str(request.POST.get('txtValue', ''))
        if id == -1:    # new object
            if Global.set(slug, value):
                return HttpResponse('ok')
            else:
                return HttpResponse('Global value save error')
        else:   # save object
            if Global.set(slug, value):
                return HttpResponse('ok')
            else:
                return HttpResponse('Global value save error')
    elif id is None:
        # return admin form
        return render(request, 'admin/toolbox/global.html')
    elif id == '0':
        # return all in json
        data = serializers.serialize('json', Global.objects.all())
        return JsonResponse('{"items": %s}' % data, safe=False)
    else:
        # return one in json
        g = Global.objects.all().filter(id=id).first()
        if g is None:
            g = Global(
                id=-1,
                slug='new_global',
                value='new global'
            )
        data = serializers.serialize('json', [g, ])
        return JsonResponse('{"items": %s}' % data, safe=False)


@login_required()
@user_passes_test(admin_check)
def tag(request, id=None):
    data = None
    if request.POST:
        # save data
        id = int(request.POST.get('id', 0))
        slug = str(request.POST.get('txtSlug', 'tag'))
        name = str(request.POST.get('txtName', 'tag'))
        deleted = False
        if request.POST['deleted'] == 'true':
            deleted = True
        if id == -1:    # new object
            if not Tag.exist(slug):
                tag = Tag.objects.create(
                    slug=slug,
                    name=name,
                    deleted=deleted
                )
                tag.save()
                return HttpResponse('ok')
            else:
                return HttpResponse('Tag already exist')
        else:   # save object
            tag = Tag.objects.get(id=id)
            if tag:
                if ((tag.slug != slug) and (not Tag.exist(slug))) or (tag.slug == slug):
                    tag.slug = slug
                    tag.name = name
                    tag.deleted = deleted
                    tag.save()
                    return HttpResponse('ok')
                else:
                    return HttpResponse('Tag already exist')
            else:
                return HttpResponse('Error get object')
    elif id is None:
        # return admin form
        return render(request, 'admin/blog/tag.html')
    elif id == '0':
        # return all in json
        data = serializers.serialize('json', Tag.objects.all())
        return JsonResponse('{"items": %s}' % data, safe=False)
    else:
        # return one in json
        tag = Tag.objects.all().filter(id=id).first()
        if tag is None:
            tag = Tag(
                id=-1,
                slug='new_tag',
                name='new tag'
            )
        data = serializers.serialize('json', [tag, ])
        return JsonResponse('{"items": %s}' % data, safe=False)


@login_required()
@user_passes_test(admin_check)
def category(request, id=None):
    data = None
    if request.POST:
        # save data
        id = int(request.POST.get('id', 0))
        slug = str(request.POST.get('txtSlug', 'caregory'))
        name = str(request.POST.get('txtName', 'category'))
        order = int(request.POST.get('txtOrder', 10))
        deleted = False
        if request.POST['deleted'] == 'true':
            deleted = True
        if id == -1:    # new object
            if not Category.exist(slug):
                category = Category.objects.create(
                    slug=slug,
                    name=name,
                    deleted=deleted,
                    order=order
                )
                category.save()
                return HttpResponse('ok')
            else:
                return HttpResponse('Category already exist')
        else:   # save object
            category = Category.objects.get(id=id)
            if category:
                if ((category.slug != slug) and (not Category.exist(slug))) or (category.slug == slug):
                    category.slug = slug
                    category.name = name
                    category.deleted = deleted
                    category.order = order
                    category.save()
                    return HttpResponse('ok')
                else:
                    return HttpResponse('Category already exist')
            else:
                return HttpResponse('error get object')
    elif id is None:
        # return admin form
        return render(request, 'admin/blog/category.html')
    elif id == '0':
        # return all in json
        data = serializers.serialize('json', Category.objects.all())
        return JsonResponse('{"items": %s}' % data, safe=False)
    else:
        # return on in json
        category = Category.objects.all().filter(id=id).first()
        if category is None:
            category = Category(
                id=-1,
                slug='new_category',
                name='new category',
                order=10
            )
        data = serializers.serialize('json', [category, ])
        return JsonResponse('{"items": %s}' % data, safe=False)


@login_required()
@user_passes_test(admin_check)
def post(request, id=None):
    data = None
    if request.POST:
        # save data
        id = int(request.POST.get('id', 0))
        slug = str(request.POST.get('txtSlug', ''))
        title = str(request.POST.get('txtTitle', ''))
        status = int(request.POST.get('status', 0))
        published = request.POST.get('txtPublished', None)
        description = str(request.POST.get('txtDescription', ''))
        keywords = str(request.POST.get('txtKeywords', ''))
        teaser = str(request.POST.get('txtTeaser', ''))
        content = str(request.POST.get('txtContent', ''))
        categories = request.POST.getlist('_category', [])
        tags = request.POST.getlist('_tag', [])
        sticked = False
        comments_enabled = False
        comments_moderated = False
        do_ping = False
        if request.POST.get('sticked', '') == 'on':
            sticked = True
        if request.POST.get('comments_enabled', '') == 'on':
            comments_enabled = True
        if request.POST.get('comments_moderated', '') == 'on':
            comments_moderated = True
        if request.POST.get('do_ping', 'false') == 'on':
            do_ping = True
        if published:
            published = parse_datetime(published.replace('/', '-'))
        else:
            published = None
        if id > 0:
            post = Post.objects.get(id=id)
            if post:
                post.slug = slug
                post.title = title
                post.status = status
                post.published = published
                post.description = description
                post.keywords = keywords
                post.teaser = teaser
                post.content_prev = post.content
                post.content = content
                post.sticked = sticked
                post.comments_enabled = comments_enabled
                post.comments_moderated = comments_moderated
                post.do_ping = do_ping
                post.categories.clear()
                for _category in categories:
                    c = Category.objects.filter(slug=_category).first()
                    if c:
                        post.categories.add(c)
                post.tags.clear()
                for _tag in tags:
                    t = Tag.objects.filter(slug=_tag).first()
                    if t:
                        post.tags.add(t)
                post.save()
                return HttpResponse('ok')
            else:
                return HttpResponse('error get object')
        else:
            return HttpResponse('new')
    elif id is None:
        # return admin form
        return render(request, 'admin/blog/post.html')
    elif id == '0':
        # return all in json
        data = serializers.serialize('json', Post.objects.all().order_by('status', 'created'))
        jdata = json.loads(data)
        for _jdata in jdata:
            _jdata['fields']['statusname'] = Post.STATUS_CHOICES[_jdata['fields']['status']][1]
        data = json.dumps(jdata)
        return JsonResponse('{"items": %s}' % data, safe=False)
    else:
        # return on in json
        post = Post.objects.all().filter(id=id).first()
        if post is None:
            post = Post(
                id=-1
            )
        data = serializers.serialize('json', [post, ])
        return JsonResponse('{"items": %s}' % data, safe=False)


@login_required()
@user_passes_test(admin_check)
def post_tag(request):
    data = []
    id = request.GET.get('id', '0')
    post = Post.objects.all().filter(id=id).first()
    data = serializers.serialize('json', Tag.objects.all())
    jdata = json.loads(data)
    if post:
        for _jdata in jdata:
            for tag in post.tags.all():
                if tag.slug == _jdata['fields']['slug']:
                    _jdata['fields']['select'] = True
    data = json.dumps(jdata)
    return JsonResponse('{"items": %s}' % data, safe=False)


@login_required()
@user_passes_test(admin_check)
def post_category(request):
    data = []
    id = request.GET.get('id', '0')
    post = Post.objects.all().filter(id=id).first()
    data = serializers.serialize('json', Category.objects.all())
    jdata = json.loads(data)
    if post:
        for _jdata in jdata:
            for cat in post.categories.all():
                if cat.slug == _jdata['fields']['slug']:
                    _jdata['fields']['select'] = True
    data = json.dumps(jdata)
    return JsonResponse('{"items": %s}' % data, safe=False)


@login_required()
@user_passes_test(admin_check)
def post_preview(request):
    if request.POST:
        post = Post(
            title=request.POST.get('txtTitle', '---'),
            teaser=request.POST.get('txtTeaser', '---'),
            content=request.POST.get('txtContent', '---'),
        )
        categories = []
        tags = []
        for slug in request.POST.getlist('_category', []):
            c = Category.objects.all().filter(slug=slug).first()
            if c:
                categories.append(c)
        for slug in request.POST.getlist('_tag', []):
            t = Tag.objects.all().filter(slug=slug).first()
            if t:
                tags.append(t)
        content = {
            'post': post,
            'categories': categories,
            'tags': tags
        }
        return render(
            request,
            'admin/blog/preview.html',
            content
        )
    else:
        HttpResponse('---')


@login_required()
@user_passes_test(admin_check)
def mylink(request, id=None):
    data = None
    if request.POST:
        # save data
        id = int(request.POST.get('id'), 0)
        slug = str(request.POST.get('txtSlug', 'mylink'))
        name = str(request.POST.get('txtName', 'mylink'))
        link = str(request.POST.get('txtLink', 'mylink'))
        order = int(request.POST.get('txtOrder', 10))
        deleted = False
        blank = False
        if request.POST.get('deleted') == 'true':
            deleted = True
        if request.POST.get('blank') == 'on':
            blank = True
        if id == -1:    # new object
            if not MyLink.exist(slug):
                mylink = MyLink.objects.create(
                    slug=slug,
                    name=name,
                    link=link,
                    deleted=deleted,
                    order=order,
                    blank=blank
                )
                mylink.save()
                return HttpResponse('ok')
            else:
                return HttpResponse('Category already exist')
        else:   # save object
            mylink = MyLink.objects.get(id=id)
            if mylink:
                if ((mylink.slug != slug) and (not MyLink.exist(slug))) or (mylink.slug == slug):
                    mylink.slug = slug
                    mylink.name = name
                    mylink.link = link
                    mylink.deleted = deleted
                    mylink.blank = blank
                    mylink.order = order
                    mylink.save()
                    return HttpResponse('ok')
                else:
                    return HttpResponse('Link already exist')
            else:
                return HttpResponse('error get object')
    elif id is None:
        # return admin form
        return render(request, 'admin/links/mylink.html')
    elif id == '0':
        # return all in json
        data = serializers.serialize('json', MyLink.objects.all())
        return JsonResponse('{"items": %s}' % data, safe=False)
    else:
        # return on in json
        mylink = MyLink.objects.all().filter(id=id).first()
        if mylink is None:
            mylink = MyLink(
                id=-1,
                slug='new_link',
                name='new link',
                link='http://',
                order=10
            )
        data = serializers.serialize('json', [mylink, ])
        return JsonResponse('{"items": %s}' % data, safe=False)


@login_required()
@user_passes_test(admin_check)
def media_folder(request, id=None):
    data = None
    if request.POST:
        # save data
        id = int(request.POST.get('id'), 0)
        name = str(request.POST.get('txtName', 'New folder'))
        description = str(request.POST.get('txtDescription', ''))
        deleted = False
        if request.POST.get('deleted') == 'true':
            deleted = True
        if id == -1:    # new object
            if not Folder.exist(name, request.user):
                folder = Folder.objects.create(
                    uuid=str(uuid4()),
                    name=name,
                    description=description,
                    deleted=deleted,
                    author_id=request.user.id
                )
                folder.save()
                return HttpResponse('ok')
            else:
                return HttpResponse('Folder already exist')
        else:   # save object
            folder = Folder.objects.get(id=id)
            if folder:
                if ((folder.name != name) and (not folder.exist(name, request.user))) or (folder.name == name):
                    folder.uuid = str(uuid4())
                    folder.name = name
                    folder.description = description
                    folder.author_id = request.user.id
                    folder.deleted = deleted
                    folder.save()
                    return HttpResponse('ok')
                else:
                    return HttpResponse('Folder already exist')
            else:
                return HttpResponse('error get object')
    elif id is None:
        # return admin form
        return render(request, 'admin/media/folder.html')
    elif id == '0':
        # return all in json
        data = serializers.serialize('json', Folder.objects.all())
        return JsonResponse('{"items": %s}' % data, safe=False)
    else:
        # return on in json
        folder = Folder.objects.all().filter(id=id).first()
        if folder is None:
            folder = Folder(
                id=-1,
                uuid=str(uuid4()),
                name='new folder',
                description='',
                deleted=False,
                author_id=request.user.id
            )
        data = serializers.serialize('json', [folder, ])
        return JsonResponse('{"items": %s}' % data, safe=False)


@login_required()
@user_passes_test(admin_check)
def media_files(request, id=None):
    data = None
    folder = Folder.objects.all().filter(id=id).first()
    if folder:
        data = serializers.serialize('json', File.objects.all().filter(folder=folder, deleted=False))
        return JsonResponse('{"items": %s}' % data, safe=False)
    else:
        return HttpResponse('')


@login_required()
@user_passes_test(admin_check)
def media_file(request, id=None):
    data = None
    if request.POST:
        id = int(request.POST.get('id'), 0)
        deleted = False
        if request.POST.get('deleted') == 'true':
            deleted = True
        if id == -1:    # new object
            return HttpResponse('New file must be uploaded')
        else:   # save object
            file = File.objects.get(id=id)
            if file:
                file.deleted = deleted
                file.save()
                return HttpResponse('ok')
            else:
                return HttpResponse('error get object')
    elif id is None:
        # return admin form
        return render(request, 'admin/media/file.html')
    elif id == '0':
        # return all in json
        data = serializers.serialize('json', File.objects.all().order_by('folder'))
        jdata = json.loads(data)
        for _jdata in jdata:
            folder = Folder.objects.get(id=_jdata['fields']['folder'])
            _jdata['fields']['foldername'] = folder.name
        data = json.dumps(jdata)
        return JsonResponse('{"items": %s}' % data, safe=False)
    else:
        file = File.objects.all().filter(id=id).first()
        action = request.GET.get('action', '')
        if action == 'delete':
            file.deleted = True
            file.save()
            return HttpResponse('ok')
        else:
            data = serializers.serialize('json', [file, ])
            jdata = json.loads(data)
            folder = Folder.objects.get(id=jdata[0]['fields']['folder'])
            jdata[0]['fields']['foldername'] = folder.name
            data = json.dumps(jdata)
            return JsonResponse('{"items": %s}' % data, safe=False)


@login_required()
@user_passes_test(admin_check)
def upload(request):
    if request.POST:
        user = request.user;
        files = request.FILES.getlist('file', [])
        uuid = request.POST.get('folder', '')
        folder = Folder.objects.all().filter(uuid=uuid).first()
        if folder is None:
            folder = Folder.objects.all().filter(name='default', author=request.user).first()
            if folder is None:
                folder = Folder.objects.create(
                    uuid=str(uuid4()),
                    name='default',
                    author=user,
                )
                folder.save()
        for file in files:
            uuid = str(uuid4())
            dist = os.path.join(os.path.join(os.path.join(UPLOAD_DIR, uuid[0:1]), uuid[1:2]), uuid)
            _file = os.path.join(dist, file.name)
            image = False
            if not os.path.exists(dist):
                os.makedirs(dist)
            __file = open(_file, 'wb+')
            for chunk in file.chunks():
                __file.write(chunk)
            __file.close()
            if what(_file):
                image = True
            else:
                image = False
                create_icon(_file)
            mfile = File.objects.create(
                uuid=uuid,
                name=file.name,
                folder=folder,
                image=image,
                author=user
            )
            mfile.save()
        return HttpResponse('ok')
    else:
        return HttpResponse('error')

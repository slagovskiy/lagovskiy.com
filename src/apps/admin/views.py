from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.userext.utils import admin_check
from apps.blog.models import Tag, Category, Post
from apps.links.models import MyLink


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
        pass
    elif id is None:
        # return admin form
        return render(request, 'admin/blog/post.html')
    elif id == '0':
        # return all in json
        data = serializers.serialize('json', Post.objects.all().order_by('status', 'created'))
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

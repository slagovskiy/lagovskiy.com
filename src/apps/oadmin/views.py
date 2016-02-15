from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from apps.blog.models import Tag, Category
from apps.links.models import MyLink


def admin_check(request):
    if not request.user.is_anonymous():
        if request.user.is_admin():
            pass

def index(request):
    content = {
    }
    return render(request, 'oadmin/index.html', content)


def tag(request, id=None):
    data = None
    if request.POST:
        # save data
        id = int(request.POST['id'])
        slug = str(request.POST['txtSlug'])
        name = str(request.POST['txtName'])
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
        return render(request, 'oadmin/blog/tag.html')
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


def category(request, id=None):
    data = None
    if request.POST:
        # save data
        id = int(request.POST['id'])
        slug = str(request.POST['txtSlug'])
        name = str(request.POST['txtName'])
        order = int(request.POST['txtOrder'])
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
        return render(request, 'oadmin/blog/category.html')
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


def mylinks(request, id=None):
    data = None
    if request.POST:
        # save data
        id = int(request.POST.get('id'))
        slug = str(request.POST.get('txtSlug'))
        name = str(request.POST.get('txtName'))
        link = str(request.POST.get('txtLink'))
        order = int(request.POST.get('txtOrder'))
        deleted = False
        new_window = False
        if request.POST.get('deleted') == 'true':
            deleted = True
        if request.POST.get('new_window') == 'on':
            new_window = True
        if id == -1:    # new object
            if not MyLink.exist(slug):
                mylink = MyLink.objects.create(
                    slug=slug,
                    name=name,
                    link=link,
                    deleted=deleted,
                    order=order
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
                    mylink.new_window = new_window
                    mylink.order = order
                    mylink.save()
                    return HttpResponse('ok')
                else:
                    return HttpResponse('Link already exist')
            else:
                return HttpResponse('error get object')
    elif id is None:
        # return admin form
        return render(request, 'oadmin/links/mylink.html')
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

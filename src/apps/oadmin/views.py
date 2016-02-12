from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from apps.blog.models import Tag, Category
from apps.links.models import MyLinks


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
        return JsonResponse(data, safe=False)
    else:
        # return one in json
        tag = Tag.objects.all().filter(id=id)
        if id == -1:
            tag.slug = 'new_tag'
            tag.name = 'new tag'
        data = serializers.serialize('json', tag)
        return JsonResponse(data, safe=False)


def category(request, id=None):
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
            if not Category.exist(slug):
                category = Category.objects.create(
                    slug=slug,
                    name=name,
                    deleted=deleted
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
        return JsonResponse(data, safe=False)
    else:
        # return on in json
        category = Category.objects.all().filter(id=id)
        if id == -1:
            category.slug = 'new_category'
            category.name = 'new category'
        data = serializers.serialize('json', category)
        return JsonResponse(data, safe=False)


def mylinks(request):
    content = {
    }
    return render(request, 'oadmin/links/mylinks.html', content)


def mylinks_all(request):
    data = serializers.serialize('json', MyLinks.objects.all())
    return JsonResponse(data, safe=False)


def mylinks_edit(request, id):
    data = serializers.serialize('json', MyLinks.objects.all().filter(id=id))
    return JsonResponse(data, safe=False)


def mylinks_save(request):
    try:
        id = int(request.POST['id'])
        link = str(request.POST['txtLink'])
        order = int(request.POST['txtOrder'])
        name = str(request.POST['txtName'])
        new_window = ('txtNewW' in request.POST)
        deleted = False
        if request.POST['deleted'] == 'true':
            deleted = True
        if id == -1:
            mylink = MyLinks.objects.create(
                link=link,
                order=order,
                name=name,
                new_window=new_window,
                deleted=deleted
            )
            mylink.save()
            return HttpResponse('ok')
        else:
            mylink = MyLinks.objects.get(id=id)
            if mylink:
                mylink.url = link
                mylink.name = name
                mylink.order = order
                mylink.new_window = new_window
                mylink.deleted = deleted
                mylink.save()
                return HttpResponse('ok')
            else:
                return HttpResponse('error get object')
    except Exception as ex:
        print(ex)
        return HttpResponse(ex)

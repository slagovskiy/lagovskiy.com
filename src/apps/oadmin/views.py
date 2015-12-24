from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from apps.blog.models import Tag, Category
from apps.links.models import MyLinks


def index(request):
    content = {
    }
    return render(request, 'oadmin/index.html', content)


def tag(request):
    content = {
    }
    return render(request, 'oadmin/blog/tag.html', content)


def tag_all(request):
    data = serializers.serialize('json', Tag.objects.all())
    return JsonResponse(data, safe=False)


def tag_edit(request, id):
    data = serializers.serialize('json', Tag.objects.all().filter(id=id))
    return JsonResponse(data, safe=False)


def tag_save(request):
    try:
        id = int(request.POST['id'])
        slug = str(request.POST['txtSlug'])
        name = str(request.POST['txtName'])
        deleted = False
        if request.POST['deleted'] == 'true':
            deleted = True
        if id == -1:
            tag = Tag.objects.create(
                slug=slug,
                name=name,
                deleted=deleted
            )
            tag.save()
            return HttpResponse('ok')
        else:
            tag = Tag.objects.get(id=id)
            if tag:
                tag.slug = slug
                tag.name = name
                tag.deleted = deleted
                tag.save()
                return HttpResponse('ok')
            else:
                return HttpResponse('error get object')
    except Exception as ex:
        return HttpResponse(ex)


def category(request):
    content = {
    }
    return render(request, 'oadmin/blog/category.html', content)


def category_all(request):
    data = serializers.serialize('json', Category.objects.all())
    return JsonResponse(data, safe=False)


def category_edit(request, id):
    data = serializers.serialize('json', Category.objects.all().filter(id=id))
    return JsonResponse(data, safe=False)


def category_save(request):
    try:
        id = int(request.POST['id'])
        slug = str(request.POST['txtSlug'])
        name = str(request.POST['txtName'])
        deleted = False
        if request.POST['deleted'] == 'true':
            deleted = True
        if id == -1:
            category = Category.objects.create(
                slug=slug,
                name=name,
                deleted=deleted
            )
            category.save()
            return HttpResponse('ok')
        else:
            category = Category.objects.get(id=id)
            if category:
                category.slug = slug
                category.name = name
                category.deleted = deleted
                category.save()
                return HttpResponse('ok')
            else:
                return HttpResponse('error get object')
    except Exception as ex:
        return HttpResponse(ex)


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
        url = str(request.POST['txtUrl'])
        order = int(request.POST['txtOrder'])
        name = str(request.POST['txtName'])
        deleted = False
        if request.POST['deleted'] == 'true':
            deleted = True
        if id == -1:
            mylink = MyLinks.objects.create(
                url=url,
                order=order,
                name=name,
                deleted=deleted
            )
            mylink.save()
            return HttpResponse('ok')
        else:
            mylink = MyLinks.objects.get(id=id)
            if mylink:
                mylink.url = url
                mylink.name = name
                mylink.order = order
                mylink.deleted = deleted
                mylink.save()
                return HttpResponse('ok')
            else:
                return HttpResponse('error get object')
    except Exception as ex:
        print(ex)
        return HttpResponse(ex)

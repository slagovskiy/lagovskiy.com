from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from apps.blog.models import Tag


def index(request):
    content = {
    }
    return render(request, 'oadmin/index.html', content)


def tag(request):
    content = {
    }
    return render(request, 'oadmin/tag.html', content)


def tag_all(request):
    data = serializers.serialize('json', Tag.objects.all())
    return JsonResponse(data, safe=False)


def tag_save(request):
    id = int(request.POST['id'])
    slug = str(request.POST['txtSlug'])
    name = str(request.POST['txtName'])
    tag = Tag.objects.get(id=id)
    if tag:
        tag.slug = slug
        tag.name = name
        tag.save()
        return HttpResponse('ok')
    else:
        return HttpResponse('error')


def tag_edit(request, id):
    data = serializers.serialize('json', Tag.objects.all().filter(id=id))
    return JsonResponse(data, safe=False)

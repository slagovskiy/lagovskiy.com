from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
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


def tag_edit(request, id):
    data = serializers.serialize('json', Tag.objects.all().filter(id=id))
    return JsonResponse(data, safe=False)

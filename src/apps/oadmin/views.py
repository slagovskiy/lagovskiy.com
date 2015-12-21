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

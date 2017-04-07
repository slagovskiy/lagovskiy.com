from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

from .settings import PAGE_SIZE


def photo_view(request):
    page = int(request.GET.get('page', 1))
    photos = []#Photo.objects.all().filter(status=Photo.PUBLISHED_STATUS).order_by('-published')
    paginator = Paginator(photos, PAGE_SIZE)
    if page <= 0:
        page = 1
        if page > paginator.num_pages:
            page = paginator.num_pages

    content = {
        'photos': paginator.page(page)
    }
    return render(request, 'photo/index.html', content)


def photo_by_album(request):
    content = []
    return  render(request, 'photo/index.html', content)


def photo_by_tag(request):
    content = []
    return  render(request, 'photo/index.html', content)
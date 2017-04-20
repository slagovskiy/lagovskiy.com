from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

from .settings import PAGE_SIZE
from .models import Album, Tag, Photo


def photo_view(request):
    page = int(request.GET.get('page', 1))
    photos = Photo.objects.all().filter(status=Photo.PUBLISHED_STATUS).order_by('published')
    paginator = Paginator(photos, PAGE_SIZE)
    if page <= 0:
        page = 1
        if page > paginator.num_pages:
            page = paginator.num_pages

    content = {
        'photos': paginator.page(page)
    }
    return render(request, 'photo/index.html', content)


def photo_by_album(request, slug=''):
    page = int(request.GET.get('page', 1))
    album = Album.objects.filter(slug=slug).first()
    photos = album.photo_set.filter(status=Photo.PUBLISHED_STATUS).order_by('published')
    paginator = Paginator(photos, PAGE_SIZE)
    if page <= 0:
        page = 1
        if page > paginator.num_pages:
            page = paginator.num_pages

    content = {
        'photos': paginator.page(page),
        'active_album': album
    }
    return render(request, 'photo/index.html', content)


def photo_by_tag(request, slug=''):
    page = int(request.GET.get('page', 1))
    tag = Tag.objects.filter(slug=slug).first()
    photos = tag.photo_set.filter(status=Photo.PUBLISHED_STATUS).order_by('published')
    paginator = Paginator(photos, PAGE_SIZE)
    if page <= 0:
        page = 1
        if page > paginator.num_pages:
            page = paginator.num_pages

    content = {
        'photos': paginator.page(page),
        'active_phototag': tag
    }
    return render(request, 'photo/index.html', content)


def photo_item_view(request, slug=''):
    photo = Photo.objects.all().filter(slug=slug, status=Photo.PUBLISHED_STATUS).first()
    content = {
        'photo': photo
    }
    return render(request, 'photo/photo_view.html', content)

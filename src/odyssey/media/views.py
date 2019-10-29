import os
from sendfile import sendfile
from .models import MediaFolder, MediaFile
from ..settings import UPLOAD_DIR
from django.http import JsonResponse, HttpResponse

from ..settings import MEDIA_ROOT
from ..settings import STATIC_DIR
from ..toolbox.image import image_resize, what


def media(request, path):
    file_path = os.path.join(MEDIA_ROOT, path)
    if os.path.exists(file_path):
        if len(request.GET) > 0:
            if not what(file_path):
                if request.GET.get('img', '') != '':
                    file_path = os.path.join(STATIC_DIR, 'img/image-not-found.jpg')
                else:
                    return sendfile(request, file_path)
            if 'w' in request.GET:
                _file_path = image_resize(file_path, 'w', request.GET.get('w', 600))
            if 'h' in request.GET:
                _file_path = image_resize(file_path, 'h', request.GET.get('h', 600))
            if 's' in request.GET:
                _file_path = image_resize(file_path, 's', request.GET.get('s', 600))
            if _file_path:
                file_path = _file_path
    else:
        file_path = os.path.join(STATIC_DIR, 'img/image-not-found.jpg')
    return sendfile(request, file_path)

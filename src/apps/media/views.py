import os
from PIL import Image
from sendfile import sendfile
from django.http import HttpResponse, Http404
from .models import File
from odyssey.settings import UPLOAD_URL, UPLOAD_DIR


def media_file(request, key=None, filename=None):
    file = File.objects.all().filter(uuid=key).first()
    file_path = ''
    filename = ''
    _file_path = False
    if file:
        if file.image:
            filename = file.name
        else:
            filename = 'icon.jpg'
        file_path = os.path.join(os.path.join(os.path.join(os.path.join(
            UPLOAD_DIR, file.uuid[0:1]), file.uuid[1:2]), file.uuid), filename)
        if 'w' in request.GET:
            _file_path = image_resize(file_path, 'w', request.GET.get('w', 600))
        if 'h' in request.GET:
            _file_path = image_resize(file_path, 'h', request.GET.get('h', 600))
        if 's' in request.GET:
            _file_path = image_resize(file_path, 's', request.GET.get('s', 600))
        if _file_path:
            file_path = _file_path
        return sendfile(request, file_path)
    else:
        raise Http404


def image_resize(imagefile, type, size):
    save = False
    filename = os.path.join(os.path.dirname(imagefile), type + str(size) + '.jpg')
    try:
        if os.path.exists(filename):
            return filename
        size = int(size)
        source = Image.open(imagefile)
        if type == 'w':
            if source.size[0] > size:
                wpercent = (size/float(source.size[0]))
                hsize = int((float(source.size[1])*float(wpercent)))
                source = source.resize((size, hsize), Image.ANTIALIAS)
            save = True
        elif type == 'h':
            if source.size[1] > size:
                wpercent = (size/float(source.size[1]))
                hsize = int((float(source.size[0])*float(wpercent)))
                source = source.resize((hsize, size), Image.ANTIALIAS)
            save = True
        elif type == 's':
            if source.size[0] < source.size[1]:
                wpercent = (size/float(source.size[0]))
                hsize = int((float(source.size[1])*float(wpercent)))
                source = source.resize((size, hsize), Image.ANTIALIAS)
                left = 0
                top = int((source.size[1]/2)-(size/2))
                right = size
                bottom = int((source.size[1]/2)+(size/2))
                source = source.crop((left, top, right, bottom))
                save = True
            else:
                wpercent = (size/float(source.size[1]))
                hsize = int((float(source.size[0])*float(wpercent)))
                source = source.resize((hsize, size), Image.ANTIALIAS)
                left = int((source.size[0]/2)-(size/2))
                top = 0
                right = int((source.size[0]/2)+(size/2))
                bottom = size
                source = source.crop((left, top, right, bottom))
                save = True
        if save:
            source.save(filename)
            return filename
        else:
            return False
    except:
        return False

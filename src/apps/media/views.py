import os
from sendfile import sendfile
from django.http import HttpResponse
from .models import File
from odyssey.settings import UPLOAD_URL, UPLOAD_DIR


def media_file(request, key=None):
    file = File.objects.all().filter(uuid=key).first()
    file_path = ''
    file_url = ''
    if file:
        file_path = os.path.join(
            os.path.join(
                os.path.join(
                    os.path.join(UPLOAD_DIR, file.uuid[0:1]),
                    file.uuid[1:2]
                ),
                file.uuid
            ),
            file.name
        )
        file_url = UPLOAD_URL + file.uuid[0:1] + '/' + file.uuid[1:2] + '/' + file.uuid + '/' + file.name
        return sendfile(request, file_path)
    else:
        HttpResponse('')

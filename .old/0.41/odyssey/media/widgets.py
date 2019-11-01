from django.template.loader import render_to_string
from .models import MediaFolder, MediaFile


def MediaLib():
    folders = MediaFolder.objects.all()
    files = MediaFile.objects.filter(folder=None)
    return render_to_string('media/widget.html', {
        'folders': folders,
        'files': files
    })

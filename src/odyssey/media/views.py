import os
from sendfile import sendfile
from rest_framework.parsers import FileUploadParser, MultiPartParser, JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import MediaFolder, MediaFile
from ..settings import UPLOAD_DIR
from .serializers import MediaFolderSerializer, MediaFileSerializer
from django.http import JsonResponse, HttpResponse

from ..settings import MEDIA_ROOT, STATIC_ROOT
from ..toolbox.image import image_resize, what


def media(request, path):
    file_path = os.path.join(MEDIA_ROOT, path)
    if os.path.exists(file_path):
        if len(request.GET) > 0:
            if not what(file_path):
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
        file_path = os.path.join(STATIC_ROOT, 'img/image-not-found.jpg')
    return sendfile(request, file_path)


class APIMedia(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({

        }, status=status.HTTP_200_OK)


class APIMediaFolder(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    # permission_classes = [permissions.AllowAny,]

    def get(self, request):
        id = request.GET.get('id')
        slug = request.GET.get('slug')
        if id:
            items = MediaFolder.objects.filter(id=id)
        elif slug:
            items = MediaFolder.objects.filter(slug=slug)
        else:
            items = MediaFolder.objects.all()
        serializer = MediaFolderSerializer(items, many=True)
        return Response({
            'data': serializer.data
        })

    def post(self, request):
        data = JSONParser().parse(request)
        mediafolder = None
        if 'id' in data:
            if data['id'] != -1:
                mediafolder = MediaFolder.objects.get(id=data['id'])
        item = MediaFolderSerializer(mediafolder, data=data)
        if item.is_valid():
            item.save()
            return Response({
                'data': item.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)


class APIMediaFile(APIView):
    parser_classes = [MultiPartParser, ]
    permission_classes = [permissions.IsAuthenticated, ]

    # permission_classes = [permissions.AllowAny,]

    def get(self, request):

        id = request.GET.get('id')
        folder = request.GET.get('folder')
        if id:
            items = MediaFile.objects.filter(id=id).order_by('-created')
        elif folder:
            folder = MediaFolder.objects.get(id=folder)
            items = MediaFile.objects.filter(folder=folder).order_by('-created')
        else:
            items = MediaFile.objects.all().order_by('-created')
        serializer = MediaFileSerializer(items, many=True)
        return Response({
            'data': serializer.data
        })

    def post(self, request):
        try:
            id = request.POST.get('id', '-1')
            # up_file = request.FILES['file']
            mediafile = None
            if id:
                if id != '-1':
                    mediafile = MediaFile.objects.get(id=id)
                else:
                    mediafile = MediaFile.objects.create()
                deleted = False
                if request.POST.get('deleted', 'false') == 'true':
                    deleted = True
                folder = request.POST.get('folder', -1)
                if folder:
                    if folder == 'null':
                        folder = None
                    elif folder != -1:
                        folder = MediaFolder.objects.get(id=folder)
                    else:
                        folder = None
                else:
                    folder = None
                mediafile.folder = folder
                mediafile.name = request.POST.get('name', '')
                mediafile.description = request.POST.get('description', '')
                mediafile.deleted = deleted
                mediafile.save()

                if 'file' in request.FILES:
                    up_file = request.FILES['file']
                    file = os.path.join(UPLOAD_DIR, MediaFile.mediafile_path(mediafile, up_file.name))
                    filename = os.path.basename(file)
                    if not os.path.exists(os.path.dirname(file)):
                        os.makedirs(os.path.dirname(file))
                    destination = open(file, 'wb+')
                    for chunk in up_file.chunks():
                        destination.write(chunk)
                    mediafile.file.save(filename, destination, save=False)
                    mediafile.save()
                    destination.close()

                item = MediaFileSerializer(mediafile)

            return Response({
                'data': item.data
            }, status=status.HTTP_200_OK)
        except():
            return Response({
                'data': ''
            }, status=status.HTTP_400_BAD_REQUEST)

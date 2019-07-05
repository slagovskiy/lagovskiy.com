import os
from sendfile import sendfile
from rest_framework.parsers import JSONParser
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
    permission_classes = [permissions.IsAuthenticated,]
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
    permission_classes = [permissions.IsAuthenticated,]
    # permission_classes = [permissions.AllowAny,]

    def get(self, request):
        id = request.GET.get('id')
        folder = request.GET.get('folder')
        if id:
            items = MediaFile.objects.filter(id=id)
        elif folder:
            items = MediaFile.objects.filter(folder=folder)
        else:
            items = MediaFile.objects.all()
        serializer = MediaFileSerializer(items, many=True)
        return Response({
            'data': serializer.data
        })

    def post(self, request):
        '''
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
                '''
        return Response({
            'data': ''
        }, status=status.HTTP_200_OK)


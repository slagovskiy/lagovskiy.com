from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import MediaFolder
from ..settings import UPLOAD_DIR
from .serializers import MediaFolderSerializer
from django.http import JsonResponse, HttpResponse


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

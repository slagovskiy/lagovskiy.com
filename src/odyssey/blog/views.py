from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import Category
from ..settings import UPLOAD_DIR
from .serializers import CategorySerializer
from django.http import JsonResponse, HttpResponse


class APIBlog(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({

        }, status=status.HTTP_200_OK)

class APICategory(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    # permission_classes = [permissions.AllowAny,]

    def get(self, request):
        id = request.GET.get('id')
        slug = request.GET.get('slug')
        if id:
            items = Category.objects.filter(id=id)
        elif slug:
            items = Category.objects.filter(slug=slug)
        else:
            items = Category.objects.all()
        serializer = CategorySerializer(items, many=True)
        return Response({
            'data': serializer.data
        })

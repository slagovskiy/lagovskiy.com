from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import Category, Tag, Post
from ..settings import UPLOAD_DIR
from .serializers import CategorySerializer, TagSerializer, PostSerializer
from django.http import JsonResponse, HttpResponse


class APIBlog(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({

        }, status=status.HTTP_200_OK)


class APICategory(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

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

    def post(self, request):
        data = JSONParser().parse(request)
        category = None
        if 'id' in data:
            if data['id'] != -1:
                category = Category.objects.get(id=data['id'])
        item = CategorySerializer(category, data=data)
        if item.is_valid():
            item.save()
            return Response({
                'data': item.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)


class APITag(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    # permission_classes = [permissions.AllowAny,]

    def get(self, request):
        id = request.GET.get('id')
        slug = request.GET.get('slug')
        if id:
            items = Tag.objects.filter(id=id)
        elif slug:
            items = Tag.objects.filter(slug=slug)
        else:
            items = Tag.objects.all()
        serializer = TagSerializer(items, many=True)
        return Response({
            'data': serializer.data
        })

    def post(self, request):
        data = JSONParser().parse(request)
        tag = None
        if 'id' in data:
            if data['id'] != -1:
                tag = Tag.objects.get(id=data['id'])
        item = TagSerializer(tag, data=data)
        if item.is_valid():
            item.save()
            return Response({
                'data': item.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)


class APIPost(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    # permission_classes = [permissions.AllowAny,]

    def get(self, request):
        id = request.GET.get('id')
        slug = request.GET.get('slug')
        if id:
            items = Post.objects.filter(id=id)
        elif slug:
            items = Post.objects.filter(slug=slug)
        else:
            items = Post.objects.all().order_by('status', '-created')
        serializer = PostSerializer(items, many=True)
        return Response({
            'data': serializer.data
        })

    def post(self, request):
        '''
                data = JSONParser().parse(request)
                tag = None
                if 'id' in data:
                    if data['id'] != -1:
                        tag = Tag.objects.get(id=data['id'])
                item = TagSerializer(tag, data=data)
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
            'ok': 'ok'
        }, status=status.HTTP_200_OK)

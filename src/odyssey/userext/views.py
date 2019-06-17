import os
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import UpdateAPIView
from rest_framework.parsers import FileUploadParser, MultiPartParser, JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import User
from ..settings import UPLOAD_DIR
from .serializers import UserSerializer, ChangePasswordSerializer, AvatarSerializer, UserInfoSerializer, NewUserSerializer, RestoreUserSerializer
from django.http import JsonResponse, HttpResponse


class APIUser(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    # permission_classes = [permissions.AllowAny,]

    def get(self, request):
        # email = request.GET.get('email')
        email = request.user.email
        user = User.objects.filter(email=email)
        serializer = UserSerializer(user, many=True)
        return Response({
            'data': serializer.data
        })

    def put(self, request):
        data = JSONParser().parse(request)
        user = UserSerializer(request.user, data=data)

        if user.is_valid():
            user.save()
            return Response({
                'data': user.data
            })
        else:
            return Response({
                'status': 'error'
            })


class APIUserRegister(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = JSONParser().parse(request)
        _user = User.objects.all().filter(email=data['email'])
        if _user:
            return Response({
                'status': 'User already register.'
            }, status=status.HTTP_409_CONFLICT)
        user = NewUserSerializer(data=data)
        if user.is_valid():
            user.save()
            _user = User.objects.get(email=data['email'])
            _user.set_password(data['password'])
            _user.save()
            return Response({
                'status': 'ok'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'Invalid data.'
            }, status=status.HTTP_400_BAD_REQUEST)


class APIUserRestore(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = JSONParser().parse(request)
        _user = User.objects.all().filter(email=data['email'])
        user = RestoreUserSerializer(data=data)
        if user.is_valid():
            if _user:
                return Response({
                    'status': 'User found.'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': 'User not found.'
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({
                'status': 'Wrong email.'
            }, status=status.HTTP_400_BAD_REQUEST)


class APIChangePassword(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated,]

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.data.get('old_password')):
                return Response(
                    {
                        'status': 'Wrong password'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response(
                {
                    'status': 'ok'
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIUploadAvatar(APIView):
    parser_classes = [MultiPartParser,]
    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request):
        user = request.user

        up_file = request.FILES['file']
        file = os.path.join(UPLOAD_DIR, User.avatar_path(user, up_file.name))
        filename = os.path.basename(file)
        if not os.path.exists(os.path.dirname(file)):
            os.makedirs(os.path.dirname(file))
        destination = open(file, 'wb+')
        for chunk in up_file.chunks():
            destination.write(chunk)
        user.avatar.save(filename, destination, save=False)
        user.save()
        destination.close()

        return Response(
            {
                'status': 'ok'
            },
            status=status.HTTP_200_OK
        )

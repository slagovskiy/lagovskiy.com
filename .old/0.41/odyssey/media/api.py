import os
import uuid
from django.utils import timezone
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import UpdateAPIView
from rest_framework.parsers import FileUploadParser, MultiPartParser, JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from ..settings import UPLOAD_DIR
from .serializers import MediaFileSerializer, MediaFileUploadSerializer
from .models import MediaFile, MediaFolder
from django.http import JsonResponse, HttpResponse


class APIMediaFile(APIView):
    # permission_classes = [permissions.IsAuthenticated,]
    # permission_classes = [permissions.AllowAny,]

    def get(self, request):
        user = request.user

        file_id = request.GET.get('file', None)
        folder_id = request.GET.get('folder', None)
        if folder_id:
            mediafolder = MediaFolder.objects.filter(id=folder_id)

        if file_id:
            mediafile = MediaFile.objects.filter(id=file_id)
        elif folder_id:
            if mediafolder:
                mediafile = MediaFile.objects.filter(folder=mediafolder[0])
            else:
                mediafile = []
        else:
            mediafile = MediaFile.objects.filter(folder=None)

        serializer = MediaFileSerializer(mediafile, many=True)
        return Response({
            'data': serializer.data
        })


class APIMediaFolder(APIView):
    # permission_classes = [permissions.IsAuthenticated,]
    # permission_classes = [permissions.AllowAny,]

    def get(self, request):
        user = request.user

        folder_id = request.GET.get('folder', None)

        if folder_id:
            mediafolder = MediaFolder.objects.filter(id=folder_id)
        else:
            mediafolder = MediaFolder.objects.all()

        serializer = MediaFileSerializer(mediafolder, many=True)
        return Response({
            'data': serializer.data
        })

    def post(self, request):
        return Response({
            'status': 'error'
        })

'''
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
        user = User.objects.all().filter(email=data['email'])
        if len(user) > 0:
            user = user[0]
            user.password_request_date = timezone.now()
            user.password_request_token = str(uuid.uuid1())
            user.save()
            add_email(
                msg_to=user.email,
                subject=u'Восстановление пароля на сайте HelpCrew',
                body=render_to_string('user/email_restore.html', {'user': user})
            )
            return Response({
                'status': 'User found.'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'User not found.'
            }, status=status.HTTP_404_NOT_FOUND)


class APIUserRestore2(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = JSONParser().parse(request)
        if data['token'] != '':
            user = User.objects.all().filter(password_request_token=data['token'])
            if len(user) == 1:
                user = user[0]
                if (timezone.now()-user.password_request_date).seconds < 60*60*3:
                    user.set_password(data['password'])
                    user.password_request_token = ''
                    user.save()
                    return Response({
                        'status': 'User found.'
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'status': 'Timeout.'
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    'status': 'User not found.'
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({
                'status': 'Token not found.'
            }, status=status.HTTP_404_NOT_FOUND)


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
'''

from django.urls import path
from django.conf.urls import url
from .views import APIUser, APIChangePassword, APIUploadAvatar, APIUserRegister, APIUserRestore


urlpatterns = [
    url('password/', APIChangePassword.as_view()),
    url('restore/', APIUserRestore.as_view()),
    url('register/', APIUserRegister.as_view()),
    url('avatar/', APIUploadAvatar.as_view()),
    url('', APIUser.as_view()),
]

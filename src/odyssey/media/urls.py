from django.urls import path
from django.conf.urls import url
from .views import APIMediaFolder


urlpatterns = [
#    url('password/', APIChangePassword.as_view()),
    url('folder/', APIMediaFolder.as_view())
]

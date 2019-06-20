from django.urls import path
from django.conf.urls import url
from .views import APIBlog, APICategory


urlpatterns = [
#    url('password/', APIChangePassword.as_view()),
    url('category/', APICategory.as_view()),
    url('', APIBlog.as_view()),
]

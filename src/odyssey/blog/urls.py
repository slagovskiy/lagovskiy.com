from django.urls import path
from django.conf.urls import url
from .views import APIBlog, APICategory, APITag


urlpatterns = [
#    url('password/', APIChangePassword.as_view()),
    url('category/', APICategory.as_view()),
    url('tag/', APITag.as_view()),
    url('', APIBlog.as_view()),
]

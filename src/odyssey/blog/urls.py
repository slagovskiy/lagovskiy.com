from django.urls import path
from django.conf.urls import url
from .views import APIBlog, APICategory, APITag, APIPost


urlpatterns = [
#    url('password/', APIChangePassword.as_view()),
    url('category/', APICategory.as_view()),
    url('tag/', APITag.as_view()),
    url('post/', APIPost.as_view()),
    url('', APIBlog.as_view()),
]

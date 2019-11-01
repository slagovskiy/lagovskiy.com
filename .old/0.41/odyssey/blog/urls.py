from django.urls import path
from django.conf.urls import url

from .views import blog_view, blog_post_view, blog_post_by_tag, blog_post_by_category


urlpatterns = [
    url(r'^$', blog_view, name='blog'),
    url(r'^tag/(?P<slug>[-\w]+)/$', blog_post_by_tag, name='blog_post_by_tag'),
    url(r'^category/(?P<slug>[-\w]+)/$', blog_post_by_category, name='blog_post_by_category'),
    url(r'^view/(?P<slug>[-\w]+)/$', blog_post_view, name='blog_post'),
]

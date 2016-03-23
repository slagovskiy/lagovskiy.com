from django.conf.urls import url
from .views import blog_view, blog_post_view

urlpatterns = [
    url(r'^$', blog_view, name='blog'),

    url(r'^view/(?P<slug>[-\w]+)/$', blog_post_view, name='blog_post'),
]

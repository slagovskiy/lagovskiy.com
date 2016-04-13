from django.conf.urls import url
from .views import blog_view, blog_post_view, blog_post_by_tag, blog_post_by_category, blog_comment_save, blog_comment

urlpatterns = [
    url(r'^$', blog_view, name='blog'),
    url(r'^tag/(?P<slug>[-\w]+)/$', blog_post_by_tag, name='blog_post_by_tag'),
    url(r'^category/(?P<slug>[-\w]+)/$', blog_post_by_category, name='blog_post_by_category'),
    url(r'^comment/save/', blog_comment_save, name='blog_comment_save'),
    url(r'^comment/(?P<id>[-\w]+)/', blog_comment, name='blog_comment'),
    url(r'^view/(?P<slug>[-\w]+)/$', blog_post_view, name='blog_post'),
]

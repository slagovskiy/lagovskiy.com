from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'apps.blog.views.index'),
    url(r'^archive/(?P<year>[-\w]+)/(?P<month>[-\w]+)/$', 'apps.blog.views.archive'),
    url(r'^tag/(?P<tag>[-\w]+)/$', 'apps.blog.views.postby_tag'),
    url(r'^category/(?P<category>[-\w]+)/$', 'apps.blog.views.postby_category'),
    url(r'^view/(?P<slug>[-\w]+)/$', 'apps.blog.views.post_view'),
    url(r'^comment/count/(?P<post_id>[-\w]+)/$', 'apps.blog.views.comment_count'),
    url(r'^comment/save/(?P<id>[-\w]+)/$', 'apps.blog.views.comment_save'),
    url(r'^unsubscribe/(?P<hash>[-:\w]+)/$', 'apps.blog.views.unsubscribe'),
    url(r'^message/$', 'apps.blog.views.message'),
)


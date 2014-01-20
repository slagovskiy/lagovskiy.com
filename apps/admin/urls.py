from django.conf.urls import patterns, url
from apps.admin.views import *
from apps.admin.views_stat import *
from apps.admin.views_blog_category import *
from apps.admin.views_blog_tag import *
from apps.admin.views_blog_post import *
from apps.admin.views_blog_revision import *
from apps.admin.views_blog_comment import *
from apps.admin.views_blog_image import *
from apps.admin.views_blog_subscribe import *
from apps.admin.views_blog_visitor import *
from apps.admin.views_banner import *


urlpatterns = patterns('',
                       url(r'^$', index),
                       url(r'^ad/$', ad),
                       url(r'^login/$', login_action),
                       url(r'^logout/$', logout_action),
                       url(r'^login_check/$', login_check),

                       url(r'^blog/category/getall/', blog_category_getall),
                       url(r'^blog/category/getlist/', blog_category_getlist),
                       url(r'^blog/category/save/', blog_category_save),
                       url(r'^blog/category/edit/(?P<category_id>[-\w]+)/', blog_category_edit),
                       url(r'^blog/category/moveup/(?P<category_id>[-\w]+)/', blog_category_moveup),
                       url(r'^blog/category/movedown/(?P<category_id>[-\w]+)/', blog_category_movedown),
                       url(r'^blog/category/', blog_category),

                       url(r'^blog/tag/getall/', blog_tag_getall),
                       url(r'^blog/tag/getlist/', blog_tag_getlist),
                       url(r'^blog/tag/save/', blog_tag_save),
                       url(r'^blog/tag/edit/(?P<tag_id>[-\w]+)/', blog_tag_edit),
                       url(r'^blog/tag/moveup/(?P<tag_id>[-\w]+)/', blog_tag_moveup),
                       url(r'^blog/tag/movedown/(?P<tag_id>[-\w]+)/', blog_tag_movedown),
                       url(r'^blog/tag/', blog_tag),

                       url(r'^blog/post/getall/', blog_post_getall),
                       url(r'^blog/post/save/', blog_post_save),
                       url(r'^blog/post/edit/(?P<post_id>[-\w]+)/', blog_post_edit),
                       url(r'^blog/post/', blog_post),

                       url(r'^blog/postimage/save/', blog_postimage_save),
                       url(r'^blog/postimage/delete/(?P<image_id>[-\w]+)', blog_postimage_delete),
                       url(r'^blog/postimage/insert/(?P<image_id>[-\w]+)', blog_postimage_insert),
                       url(r'^blog/postimage/edit/(?P<post_id>[-\w]+)/(?P<image_id>[-\w]+)', blog_postimage_edit),
                       url(r'^blog/postimage/(?P<post_id>[-\w]+)/', blog_postimage_list),

                       url(r'^blog/comment/save/', blog_comment_save),
                       url(r'^blog/comment/restore/(?P<comment_id>[-\w]+)/', blog_comment_restore),
                       url(r'^blog/comment/getlist/(?P<post_id>[-\w]+)/', blog_comment_getlist),
                       url(r'^blog/comment/edit/(?P<comment_id>[-\w]+)/', blog_comment_edit),
                       url(r'^blog/comment/delete/(?P<comment_id>[-\w]+)/', blog_comment_delete),
                       url(r'^blog/comment/allow/(?P<comment_id>[-\w]+)/', blog_comment_allow),

                       url(r'^blog/revision/getlist/(?P<post_id>[-\w]+)/', blog_revision_getlist),
                       url(r'^blog/revision/getcontent/(?P<revision_id>[-\w]+)/', blog_revision_getcontent),
                       url(r'^blog/revision/getteaser/(?P<revision_id>[-\w]+)/', blog_revision_getteaser),
                       url(r'^blog/revision/create/(?P<post_id>[-\w]+)/', blog_revision_create),
                       url(r'^blog/revision/save/(?P<post_id>[-\w]+)/', blog_revision_save),
                       url(r'^blog/revision/fix/(?P<revision_id>[-\w]+)/', blog_revision_fix),
                       url(r'^blog/revision/preview/(?P<revision_id>[-\w]+)/', blog_revision_preview),

                       url(r'^banner/getall/', banner_getall),
                       url(r'^banner/save/', banner_save),
                       url(r'^banner/edit/(?P<baner_id>[-\w]+)/', banner_edit),
                       url(r'^banner/', banner_index),

                       url(r'^visitors/date/', blog_visitors_dates),
                       url(r'^visitors/', blog_visitors_by_point),

                       url(r'^stat/', stat_index),

                       url(r'^blog/subscribe/save/', blog_subscribe_save),
                       url(r'^blog/subscribe/edit/(?P<subscribe_id>[-\w]+)/', blog_subscribe_edit),
                       url(r'^blog/subscribe/(?P<post_id>[-\w]+)/', blog_subscribe_getlist),
)
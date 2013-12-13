from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'apps.admin.views.index'),
    url(r'^ad/$', 'apps.admin.views.ad'),
    url(r'^login/$', 'apps.admin.views.login_action'),
    url(r'^logout/$', 'apps.admin.views.logout_action'),
    url(r'^login_check/$', 'apps.admin.views.login_check'),


    ####################################################
    #  blog
    ####################################################
    url(r'^blog/category/getall/', 'apps.admin.views.blog_category_getall'),
    url(r'^blog/category/getlist/', 'apps.admin.views.blog_category_getlist'),
    url(r'^blog/category/save/', 'apps.admin.views.blog_category_save'),
    url(r'^blog/category/edit/(?P<id>[-\w]+)/', 'apps.admin.views.blog_category_edit'),
    url(r'^blog/category/moveup/(?P<id>[-\w]+)/', 'apps.admin.views.blog_category_moveup'),
    url(r'^blog/category/movedown/(?P<id>[-\w]+)/', 'apps.admin.views.blog_category_movedown'),
    url(r'^blog/category/', 'apps.admin.views.blog_category'),

    url(r'^blog/tag/getall/', 'apps.admin.views.blog_tag_getall'),
    url(r'^blog/tag/getlist/', 'apps.admin.views.blog_tag_getlist'),
    url(r'^blog/tag/save/', 'apps.admin.views.blog_tag_save'),
    url(r'^blog/tag/edit/(?P<id>[-\w]+)/', 'apps.admin.views.blog_tag_edit'),
    url(r'^blog/tag/moveup/(?P<id>[-\w]+)/', 'apps.admin.views.blog_tag_moveup'),
    url(r'^blog/tag/movedown/(?P<id>[-\w]+)/', 'apps.admin.views.blog_tag_movedown'),
    url(r'^blog/tag/', 'apps.admin.views.blog_tag'),

    url(r'^blog/post/getall/', 'apps.admin.views.blog_post_getall'),
    url(r'^blog/post/save/', 'apps.admin.views.blog_post_save'),
    url(r'^blog/post/edit/(?P<id>[-\w]+)/', 'apps.admin.views.blog_post_edit'),
    url(r'^blog/post/', 'apps.admin.views.blog_post'),

    url(r'^blog/postimage/save/', 'apps.admin.views.blog_postimage_save'),
    url(r'^blog/postimage/delete/(?P<id>[-\w]+)', 'apps.admin.views.blog_postimage_delete'),
    url(r'^blog/postimage/insert/(?P<id>[-\w]+)', 'apps.admin.views.blog_postimage_insert'),
    url(r'^blog/postimage/edit/(?P<post_id>[-\w]+)/(?P<id>[-\w]+)', 'apps.admin.views.blog_postimage_edit'),
    url(r'^blog/postimage/(?P<post_id>[-\w]+)/', 'apps.admin.views.blog_postimage_list'),

    url(r'^blog/comment/getlist/(?P<id>[-\w]+)/', 'apps.admin.views.blog_comment_getlist'),
    url(r'^blog/comment/delete/(?P<id>[-\w]+)/', 'apps.admin.views.blog_comment_delete'),
    url(r'^blog/comment/restore/(?P<id>[-\w]+)/', 'apps.admin.views.blog_comment_restore'),
    url(r'^blog/comment/allow/(?P<id>[-\w]+)/', 'apps.admin.views.blog_comment_allow'),

    url(r'^blog/revision/getlist/(?P<post_id>[-\w]+)/', 'apps.admin.views.blog_revision_getlist'),
    url(r'^blog/revision/getcontent/(?P<id>[-\w]+)/', 'apps.admin.views.blog_revision_getcontent'),
    url(r'^blog/revision/getteaser/(?P<id>[-\w]+)/', 'apps.admin.views.blog_revision_getteaser'),
    url(r'^blog/revision/create/(?P<post_id>[-\w]+)/', 'apps.admin.views.blog_revision_create'),
    url(r'^blog/revision/save/(?P<post_id>[-\w]+)/', 'apps.admin.views.blog_revision_save'),
    url(r'^blog/revision/fix/(?P<id>[-\w]+)/', 'apps.admin.views.blog_revision_fix'),
    url(r'^blog/revision/preview/(?P<id>[-\w]+)/', 'apps.admin.views.blog_revision_preview'),

    url(r'^banner/getall/', 'apps.admin.views.banner_getall'),
    url(r'^banner/getlist/', 'apps.admin.views.banner_getlist'),
    url(r'^banner/save/', 'apps.admin.views.banner_save'),
    url(r'^banner/edit/(?P<id>[-\w]+)/', 'apps.admin.views.banner_edit'),
    url(r'^banner/moveup/(?P<id>[-\w]+)/', 'apps.admin.views.banner_moveup'),
    url(r'^banner/movedown/(?P<id>[-\w]+)/', 'apps.admin.views.banner_movedown'),
    url(r'^banner/', 'apps.admin.views.banner'),

    ####################################################
    #  robot
    ####################################################
    url(r'^robot/pingserver/getall/', 'apps.admin.views.robot_pingserver_getall'),
    url(r'^robot/pingserver/save/', 'apps.admin.views.robot_pingserver_save'),
    url(r'^robot/pingserver/edit/(?P<id>[-\w]+)/', 'apps.admin.views.robot_pingserver_edit'),
    url(r'^robot/pingserver/', 'apps.admin.views.robot_pingserver'),

    url(r'^robot/pingresult/date/(?P<d_y>[-\w]+).(?P<d_m>[-\w]+).(?P<d_d>[-\w]+)/(?P<id>[-\w]+)/', 'apps.admin.views.robot_pingresult_subdatepost'),
    url(r'^robot/pingresult/date/(?P<d_y>[-\w]+).(?P<d_m>[-\w]+).(?P<d_d>[-\w]+)/', 'apps.admin.views.robot_pingresult_subdate'),
    url(r'^robot/pingresult/date/', 'apps.admin.views.robot_pingresult_date'),
    url(r'^robot/pingresult/post/(?P<id>[-\w]+)/(?P<d_y>[-\w]+).(?P<d_m>[-\w]+).(?P<d_d>[-\w]+)/', 'apps.admin.views.robot_pingresult_subpostdate'),
    url(r'^robot/pingresult/post/(?P<id>[-\w]+)/', 'apps.admin.views.robot_pingresult_subpost'),
    url(r'^robot/pingresult/post/', 'apps.admin.views.robot_pingresult_post'),
    url(r'^robot/pingresult/', 'apps.admin.views.robot_pingresult'),

)



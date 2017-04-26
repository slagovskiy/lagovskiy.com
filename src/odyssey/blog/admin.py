from django.contrib import admin
from .models import Category, Tag, Post, Comment, Media
from .forms import PostAdminForm


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'deleted')
    list_filter = ('name', 'parent')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'deleted')
    ordering = ['name']


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'sticked')
    ordering = ('status', 'sticked', 'created', 'title')
    exclude = ('uid',)
    form = PostAdminForm
    readonly_fields = ('created', 'social_image_preview',)

    fieldsets = [
        (
            'general', {
                'classes': ('suit-tab suit-tab-general',),
                'fields': [
                    'slug',
                    'title',
                    'teaser',
                    'content',
                ]
            }
        ),
        (
            'status', {
                'classes': ('suit-tab suit-tab-status',),
                'fields': [
                    'status',
                    'created',
                    'published',
                    'sticked',
                    'author',
                ]
            }
        ),
        (
            'seo', {
                'classes': ('suit-tab suit-tab-seo',),
                'fields': [
                    'description',
                    'keywords',
                    'social_image',
                    'social_image_preview',
                    'do_ping',
                    'categories',
                    'tags'
                ]
            }
        ),
        (
            'comments', {
                'classes': ('suit-tab suit-tab-comments',),
                'fields': [
                    'comments_enabled',
                    'comments_moderated',
                ]
            }
        )
    ]


    #def __init__(self, *args, **kwargs):
    #    super(PostAdmin, self).__init__(*args, **kwargs)
    #    self.form.admin_site = self.admin_site

class CommentAdmin(admin.ModelAdmin):
    list_display = ('content100', 'username', 'post100', 'created', 'path', 'allowed')
    ordering = ('-created',)


class MediaAdmin(admin.ModelAdmin):
    list_display = ('media_file_admin_preview', 'title', 'description')
    ordering = ('-created',)
    exclude = ('uid', 'media_file_admin_preview')
    readonly_fields = ('media_file_preview',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Media, MediaAdmin)

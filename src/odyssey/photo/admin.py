from django.contrib import admin
from .models import Album, Tag, Photo


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'deleted')
    list_filter = ('name',)
    ordering = ['order', 'name']


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'deleted')
    list_filter = ('name',)
    ordering = ['name']


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'image_admin_preview', 'status', 'sticked')
    ordering = ('status', 'sticked', 'created', 'title')
    exclude = ('uid',)
    #form = PostAdminForm
    readonly_fields = ('created', 'image_preview',)

    fieldsets = [
        (
            'general', {
                'classes': ('',),
                'fields': [
                    'slug',
                    'title',
                    'image',
                    'image_preview'
                ]
            }
        ),
        (
            'status', {
                'classes': ('',),
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
                'classes': ('',),
                'fields': [
                    'description',
                    'keywords',
                    'albums',
                    'tags'
                ]
            }
        ),
    ]


admin.site.register(Album, AlbumAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Photo, PhotoAdmin)

from django.contrib import admin
from .models import Album, Tag, Photo, DeviceType, Device


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'deleted')
    list_filter = ('name',)
    ordering = ['order', 'name']


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'deleted')
    list_filter = ('name',)
    ordering = ['name']


class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'show_in_menu', 'deleted')
    list_filter = ('name',)
    ordering = ['name']


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'deleted')
    list_filter = ('name',)
    ordering = ['name']


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('image_admin_preview', 'title', 'slug', 'status', 'published', 'sticked')
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
                    'albums',
                    'tags',
                    'devices'
                ]
            }
        ),
    ]


admin.site.register(Album, AlbumAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(DeviceType, DeviceTypeAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Photo, PhotoAdmin)


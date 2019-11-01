from django.contrib import admin
from .models import MediaFolder, MediaFile


class MediaFolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'deleted')
    list_filter = ('name',)


class MediaFileAdmin(admin.ModelAdmin):
    list_display = ('folder', 'name', 'created', 'deleted')
    # list_filter = ('name',)


admin.site.register(MediaFolder, MediaFolderAdmin)
admin.site.register(MediaFile, MediaFileAdmin)

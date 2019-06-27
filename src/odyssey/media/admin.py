from django.contrib import admin
from .models import MediaFolder


class MediaFolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'deleted')
    list_filter = ('name',)


admin.site.register(MediaFolder, MediaFolderAdmin)

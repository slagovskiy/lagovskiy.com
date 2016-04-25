from django.contrib import admin
from .models import File
from .forms import FileAdminForm


class FileAdmin(admin.ModelAdmin):
    list_display = ['preview', 'name', 'added', 'deleted']
    ordering = ['added']
    list_filter = ['is_image', 'added']
    #form = FileAdminForm


admin.site.register(File, FileAdmin)

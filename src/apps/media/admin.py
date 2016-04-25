from django.contrib import admin
from .models import File


class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'added', 'deleted')
    list_filter = ('name', 'added')


admin.site.register(File, FileAdmin)

from django.contrib import admin
from .models import File


class FileAdmin(admin.ModelAdmin):
    list_display = ['preview', 'name', 'added', 'deleted']
    ordering = ['added']
    list_filter = ['is_image', 'added']
    readonly_fields = ['preview', 'added']
    fieldsets = [
        (None, {'fields': ['name']}),
        (None, {'fields': ['preview', 'f']}),
        (None, {'fields': ['author', 'added', 'deleted']})
    ]

admin.site.register(File, FileAdmin)

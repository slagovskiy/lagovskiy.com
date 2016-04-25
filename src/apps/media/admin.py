from django.contrib import admin
from .models import File


class FileAdmin(admin.ModelAdmin):
    list_display = ['preview', 'name', 'added', 'deleted']
    readonly_fields = ['preview', 'added']
    list_filter = ['name', 'added']
    fieldsets = [
        (None, {'fields': ['name']}),
        ('File', {'fields': ['preview', 'f']}),
        (None, {'fields': ['author', 'deleted']})
    ]

admin.site.register(File, FileAdmin)

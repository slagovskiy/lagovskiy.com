from django.contrib import admin
from .models import File
from .forms import FileAdminForm


class FileAdmin(admin.ModelAdmin):
    list_display = ['preview', 'name', 'added', 'deleted']
    ordering = ['added']
    list_filter = ['is_image', 'added']
    form = FileAdminForm

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
            obj.save()


admin.site.register(File, FileAdmin)

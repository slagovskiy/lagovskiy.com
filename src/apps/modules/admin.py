from django.contrib import admin
from .models import Module


class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'deleted')


admin.site.register(Module, ModuleAdmin)
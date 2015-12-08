from django.contrib import admin
from .models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'block', 'deleted')
    list_filter = ['block']
    ordering = ('block', 'name')


admin.site.register(Tag, TagAdmin)

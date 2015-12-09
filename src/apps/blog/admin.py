from django.contrib import admin
from .models import Category, Tag


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'deleted')
    list_filter = ('block', 'name', 'parent')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'block', 'deleted')
    list_filter = ['block']
    ordering = ('block', 'name')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)

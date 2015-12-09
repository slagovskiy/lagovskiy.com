from django.contrib import admin
from .models import Category, Tag


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'deleted')
    list_filter = ('name', 'parent')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'deleted')
    ordering = ['name']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)

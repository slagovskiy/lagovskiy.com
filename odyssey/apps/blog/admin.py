from django.contrib import admin
from .models import Category
from .models import Tag


class CategoryAdmin(admin.ModelAdmin):
    fields = ['sort', 'slug', 'name', 'deleted']
    ordering = ['sort', 'name']
    list_display = ['slug', 'name', 'sort', 'deleted']
    list_filter = ['slug']
    search_fields = ['slug']


class TagAdmin(admin.ModelAdmin):
    fields = ['sort', 'slug', 'name', 'deleted']
    ordering = ['sort', 'name']
    list_display = ['slug', 'name', 'sort', 'deleted']
    list_filter = ['slug']
    search_fields = ['slug']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)

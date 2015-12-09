from django.contrib import admin
from .models import Category, Tag, Post


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'deleted')
    list_filter = ('name', 'parent')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'deleted')
    ordering = ['name']


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'sticked')
    ordering = ('status', 'sticked', 'created', 'title')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)

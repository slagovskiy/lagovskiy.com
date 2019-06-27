from django.contrib import admin
from .models import Category, Tag


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'deleted')
    list_filter = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'deleted')
    list_filter = ('name',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)

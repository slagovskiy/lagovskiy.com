from django.contrib import admin
from .models import Category, Tag


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'deleted')
    list_filter = ('block', 'name', 'parent')


admin.site.register(Category, CategoryAdmin)

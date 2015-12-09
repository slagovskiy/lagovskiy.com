from django.contrib import admin
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'block', 'deleted')
    list_filter = ('block', 'name', 'parent')


admin.site.register(Category, CategoryAdmin)

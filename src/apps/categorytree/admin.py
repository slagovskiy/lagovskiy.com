from django.contrib import admin
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'deleted')
    list_filter = ('name', 'parent')


admin.site.register(Category, CategoryAdmin)

from django.contrib import admin
from apps.blog.models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'sort')
    search_fields = ('slug', 'name')
    ordering = ('sort',)

admin.site.register(Category, CategoryAdmin)

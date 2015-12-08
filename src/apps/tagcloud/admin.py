from django.contrib import admin
from .models import Tag


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name')


admin.site.register(Tag, TagAdmin)

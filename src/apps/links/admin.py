from django.contrib import admin
from .models import MyLink


class MyLinksAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'order')
    ordering = ('order', 'name')

admin.site.register(MyLink, MyLinksAdmin)

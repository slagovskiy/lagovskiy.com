from django.contrib import admin
from .models import MyLink
from .forms import MyLinkAdminForm


class MyLinksAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'order', 'deleted')
    ordering = ('order', 'name')
    form = MyLinkAdminForm

admin.site.register(MyLink, MyLinksAdmin)

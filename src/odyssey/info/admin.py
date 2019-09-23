from django.contrib import admin
from .models import Link


class LinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'deleted')
    list_filter = ('name',)


admin.site.register(Link, LinkAdmin)

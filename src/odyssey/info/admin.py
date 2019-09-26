from django.contrib import admin
from django.utils.html import format_html
from .models import Link


class LinkAdmin(admin.ModelAdmin):
    list_display = ('name_with_icon', 'deleted')
    list_filter = ('name',)
    readonly_fields = ('name_with_icon',)

    def name_with_icon(self, object):
        if object.icon:
            return format_html('<i class="%s"></i> %s' % (object.icon, object.name))
        else:
            return ''


admin.site.register(Link, LinkAdmin)

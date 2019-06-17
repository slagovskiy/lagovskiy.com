from django.contrib import admin
from .models import Visitor


class VisitorAdmin(admin.ModelAdmin):
    list_display = ('date', 'point', 'browser_family', 'browser_version', 'os_family', 'is_pc', 'is_bot', 'ip_address')
    ordering = ('-date',)
    readonly_fields = ('point', 'session_key', 'ip_address','user_agent', 'referer', 'date', 'browser_family',
                       'browser_version', 'os_family', 'os_version', 'device_family', 'is_mobile', 'is_tablet',
                       'is_touch_capable', 'is_pc', 'is_bot')


admin.site.register(Visitor, VisitorAdmin)

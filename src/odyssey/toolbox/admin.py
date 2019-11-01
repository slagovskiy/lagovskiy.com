from django.contrib import admin
from .models import Global, PingServer, PingResult


class GlobalAdmin(admin.ModelAdmin):
    list_display = ('slug', 'value')
    ordering = ('slug',)


class PingServerAdmin(admin.ModelAdmin):
    list_display = ('address', 'deleted')
    ordering = ('address',)


class PingResultAdmin(admin.ModelAdmin):
    list_display = ('date', 'pingserver', 'passed')
    ordering = ('-date',)

admin.site.register(Global, GlobalAdmin)
admin.site.register(PingServer, PingServerAdmin)
admin.site.register(PingResult, PingResultAdmin)

from django.contrib import admin
from userprofile.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user')
    search_fields = ('user')
    ordering = ('user',)

admin.site.register(UserProfile, UserProfileAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User



class UserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    readonly_fields = ('avatar_preview', 'last_login', 'register_date')

    list_display = [
        'email',
        'firstname',
        'lastname',
        'is_admin',
        'register_date',
        'last_login',
        'is_active'
    ]

    list_filter = ('is_admin', 'is_active')

    fieldsets = (
        ('general', {
            'classes': ('suit-tab suit-tab-general',),
            'fields': (
                'email',
                'password'
            )}),
        ('info', {
            'classes': ('suit-tab suit-tab-info',),
            'fields': (
                'avatar',
                'avatar_preview',
                'firstname',
                'lastname',
            )}),
        ('permissions', {
            'classes': ('suit-tab suit-tab-permissions',),
            'fields': (
                'is_active',
                'is_admin',
                'is_superuser',
                'groups',
                'user_permissions'
            )}),
        ('other', {
            'classes': ('suit-tab suit-tab-other',),
            'fields': (
                'last_login',
                'register_date'
            )}),
    )

    add_fieldsets = (
        ('general', {
            'classes': ('suit-tab suit-tab-general',),
            'fields': (
                'email',
                'password1',
                'password2',
            )}),
        ('info', {
            'classes': ('suit-tab suit-tab-info',),
            'fields': (
                'avatar',
                'firstname',
                'lastname',
            )}),
        ('permissions', {
            'classes': ('suit-tab suit-tab-permissions',),
            'fields': (
                'is_active',
                'is_admin',
                'is_superuser',
                'groups',
                'user_permissions'
            )}),
        ('other', {
            'classes': ('suit-tab suit-tab-other',),
            'fields': ()
        }),
    )

    suit_form_tabs = (('general', 'General'), ('info', 'Personal info'),
                      ('permissions', 'Permissions'), ('other', 'Other'))

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)

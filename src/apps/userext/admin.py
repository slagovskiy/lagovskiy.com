from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .forms import UserChangeForm
from .forms import UserCreationForm
from .models import User


class UserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

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
        (None, {
            'fields': (
                'email',
                'password'
            )}),
        ('Personal info', {
            'fields': (
                'avatar',
                'firstname',
                'lastname',
            )}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2'
            )}
         ),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models import User


class UserAdminConfig(UserAdmin):
    model = User
    save_as = True
    save_on_top = True
    list_display = (
        'first_name',
        'last_name',
        'email',
        'id',
        'is_staff',
        'is_active',
        'is_superuser',
        'is_verified',
    )
    list_display_links = (
        'first_name',
        'last_name',
        'email',
    )
    readonly_fields = ('id', 'last_login', 'date_joined')
    fieldsets = (
        (
            'Personal info',
            {'fields': ('first_name', 'last_name', 'email', 'password')},
        ),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'is_verified',
                    'groups',
                    'user_permissions',
                )
            },
        ),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(User, UserAdminConfig)

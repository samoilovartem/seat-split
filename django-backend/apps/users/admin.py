from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models import User


class UserAdminConfig(UserAdmin):
    model = User
    save_as = True
    save_on_top = True
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_active',
        'team',
        'role',
    )
    list_display_links = ('username',)
    readonly_fields = ('id', 'last_login', 'date_joined')
    fieldsets = (
        (
            'Personal info',
            {'fields': ('first_name', 'last_name', 'email', 'username', 'password')},
        ),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                    'team',
                    'role',
                )
            },
        ),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(User, UserAdminConfig)

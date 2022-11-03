from django.contrib import admin
from .models import *


class AccountsAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('title',)}
    save_as = True
    save_on_top = True
    list_display = ('id', 'account_assigned', 'platform', 'type', 'parent_card',
                    'created_by', 'team', 'updated_at')
    list_display_links = ('id', 'account_assigned')
    search_fields = ('account_assigned', 'platform', 'card_number', 'created_by__name',
                     'team__name', 'in_tm', 'in_tickets_com')
    list_filter = ('platform', 'created_by__name',
                   'team__name', 'in_tm', 'in_tickets_com')
    # readonly_fields = ('views', 'created_at', 'get_photo', 'updated_at')
    # fields = ('account_assigned', 'platform',)


class TeamsAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


class EmployeesAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('id', 'name', 'team')
    list_display_links = ('id', 'name',)


class PlatformAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


class TypeAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


admin.site.register(Accounts, AccountsAdmin)
admin.site.register(Employees, EmployeesAdmin)
admin.site.register(Teams, TeamsAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(Type, TypeAdmin)

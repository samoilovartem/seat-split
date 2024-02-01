from django.contrib import admin

from apps.stt.admin.base import BaseModelAdmin, TicketHolderTeamInline
from apps.stt.models import TicketHolder


@admin.register(TicketHolder)
class TicketHolderAdminConfig(BaseModelAdmin):
    model = TicketHolder
    save_as = True
    save_on_top = True
    ordering = ('-created_at',)
    list_display = (
        'first_name',
        'last_name',
        'get_email',
        'id',
    )
    readonly_fields = ('id', 'created_at')
    list_display_links = (
        'first_name',
        'last_name',
        'get_email',
    )
    search_fields = (
        'id',
        'first_name',
        'last_name',
        'user__email',
    )
    exclude = ('tickets_data',)
    inlines = (TicketHolderTeamInline,)
    autocomplete_fields = ('user',)

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = 'User email'

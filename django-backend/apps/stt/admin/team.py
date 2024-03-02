from django.contrib import admin

from apps.stt.admin.base import BaseModelAdmin
from apps.stt.models import Team


@admin.register(Team)
class TeamAdminConfig(BaseModelAdmin):
    model = Team
    save_as = True
    save_on_top = True
    list_display = (
        'name',
        'league',
        'city',
        'state',
        'id',
    )
    readonly_fields = ('id',)
    list_display_links = ('name',)
    search_fields = (
        'id',
        'name',
        'league',
        'city',
        'state',
    )
    list_filter = ('league',)
    autocomplete_fields = ('home_venue',)

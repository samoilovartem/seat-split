from django.contrib import admin
from django.forms import Select

from apps.stt.admin.base import BaseModelAdmin
from apps.stt.models import Team
from config.components.business_related import SUPPORTED_LEAGUES


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

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'league':
            kwargs['widget'] = Select(choices=((league, league) for league in SUPPORTED_LEAGUES))
        return super().formfield_for_dbfield(db_field, request, **kwargs)

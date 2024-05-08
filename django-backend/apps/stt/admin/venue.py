from django.contrib import admin
from django.forms import Select
from pytz import common_timezones

from apps.stt.admin.base import BaseModelAdmin
from apps.stt.models import Venue


@admin.register(Venue)
class VenueAdminConfig(BaseModelAdmin):
    model = Venue
    save_as = True
    save_on_top = True
    ordering = ('-created_at',)
    list_display = (
        'name',
        'address',
        'city',
        'state',
        'id',
    )
    readonly_fields = ('id',)
    list_display_links = ('name',)
    search_fields = (
        'id',
        'skybox_venue_id',
        'name',
        'address',
        'city',
        'state',
    )
    list_filter = ('state',)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'timezone':
            kwargs['widget'] = Select(choices=((tz, tz) for tz in common_timezones))
        return super().formfield_for_dbfield(db_field, request, **kwargs)

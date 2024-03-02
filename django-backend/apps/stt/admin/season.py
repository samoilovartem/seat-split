from datetime import datetime

from import_export.admin import ImportExportMixin
from rangefilter.filters import DateRangeFilterBuilder

from django.contrib import admin

from apps.stt.admin.base import BaseModelAdmin
from apps.stt.models import Season


@admin.register(Season)
class SeasonAdminConfig(ImportExportMixin, BaseModelAdmin):
    model = Season
    save_as = True
    save_on_top = True
    ordering = ('name',)
    list_display = (
        'name',
        'league',
        'start_year',
        'official_start_date',
        'official_end_date',
        'id',
    )
    readonly_fields = ('id',)
    list_display_links = ('name',)
    search_fields = ('id', 'name')
    list_filter = (
        'league',
        (
            'official_start_date',
            DateRangeFilterBuilder(
                title='Official start date',
                default_start=datetime.now(),
            ),
        ),
        (
            'official_end_date',
            DateRangeFilterBuilder(
                title='Official end date',
                default_start=datetime.now(),
            ),
        ),
    )

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from apps.mobile_numbers.models import MobileNumberStorage


class MobileNumberStorageAdminConfig(ImportExportModelAdmin):
    save_as = True
    save_on_top = True


admin.site.register(MobileNumberStorage, MobileNumberStorageAdminConfig)

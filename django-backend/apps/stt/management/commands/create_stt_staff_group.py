from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from config.components.business_related import STT_STAFF_GROUP_NAME, STT_STAFF_GROUP_PERMISSIONS


class Command(BaseCommand):
    help = f"Create the {STT_STAFF_GROUP_NAME} group if it doesn't exist."

    def handle(self, *args, **options):
        group_name = STT_STAFF_GROUP_NAME

        if not Group.objects.filter(name=group_name).exists():
            group = Group(name=group_name)
            group.save()

            for perm_codename in STT_STAFF_GROUP_PERMISSIONS:
                try:
                    permission = Permission.objects.get(codename=perm_codename)
                    group.permissions.add(permission)
                except Permission.DoesNotExist:
                    self.stderr.write(self.style.ERROR(f'Permission {perm_codename} not found.'))

            self.stdout.write(self.style.SUCCESS(f'Group {group_name} created successfully!'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Group {group_name} already exists.'))

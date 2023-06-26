from rest_flex_fields import FlexFieldsModelViewSet

from django.contrib.auth.models import Group, Permission
from django.db.models import Prefetch

from apps.users.api.v1.serializers import GroupSerializer


class GroupViewSet(FlexFieldsModelViewSet):
    queryset = Group.objects.all().prefetch_related(
        Prefetch('permissions', queryset=Permission.objects.only('id', 'name'))
    )
    serializer_class = GroupSerializer
    my_tags = ['All groups']
    permit_list_expands = ['permissions']

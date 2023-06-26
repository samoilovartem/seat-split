from rest_flex_fields import FlexFieldsModelViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import Group, Permission
from django.db.models import Prefetch

from apps.users.api.v1.serializers import (
    GeneralUserSerializer,
    UserCreateSerializer,
    UserDetailSerializer,
    UserListSerializer,
)
from apps.users.models import User


class UsersViewSet(FlexFieldsModelViewSet):
    queryset = User.objects.all().prefetch_related(
        Prefetch('groups', queryset=Group.objects.only('id', 'name')),
        Prefetch('user_permissions', queryset=Permission.objects.only('id', 'name')),
    )
    serializer_class = GeneralUserSerializer
    permit_list_expands = ['groups', 'user_permissions']
    my_tags = ['All users']
    serializer_class_by_action = {
        'list': UserListSerializer,
        'retrieve': UserDetailSerializer,
        'create': UserCreateSerializer,
    }

    def get_serializer_class(self):
        if hasattr(self, 'serializer_class_by_action'):
            return self.serializer_class_by_action.get(
                self.action, self.serializer_class
            )
        return super(UsersViewSet, self).get_serializer_class()

    @action(methods=['GET'], detail=False)
    def get_all_permissions_list(self, request):
        all_permissions = (
            Permission.objects.all().order_by('id').values('id', 'name', 'codename')
        )
        return Response({'results': all_permissions})

    @action(methods=['GET'], detail=False)
    def get_permissions_by_group(self, request):
        result = {
            group.name: [
                perm
                for perm in group.permissions.all().values('id', 'name', 'codename')
            ]
            for group in Group.objects.prefetch_related('permissions')
        }
        return Response({'results': result})

    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated])
    def blacklist_jwt(self, request):
        """
        Is used to blacklist a refresh_token and logout a user.
        Ex.: /api/v1/users/blacklist_jwt/?refresh_token=<refresh_token>
        """
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(data={'message': 'The token has been blacklisted'})
        except Exception as error:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': error})

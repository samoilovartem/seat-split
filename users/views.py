from django.contrib.auth.models import Permission
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .serializers import GeneralUserSerializer, UserDetailSerializer, UserListSerializer, UserCreateSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = GeneralUserSerializer
    my_tags = ["All users"]
    serializer_class_by_action = {
        'list': UserListSerializer,
        'retrieve': UserDetailSerializer,
        'create': UserCreateSerializer,
    }

    def get_serializer_class(self):
        if hasattr(self, 'serializer_class_by_action'):
            return self.serializer_class_by_action.get(self.action, self.serializer_class)
        return super(UsersViewSet, self).get_serializer_class()

    @action(methods=['GET'], detail=False)
    def get_all_permissions_list(self, request):
        all_permissions = Permission.objects.all().order_by('id').values('id', 'name', 'codename')
        return Response({'results': all_permissions})


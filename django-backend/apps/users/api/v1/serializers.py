from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework.fields import SerializerMethodField

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission

from apps.serializers import ConvertNoneToStringSerializerMixin
from apps.stt.models import TicketHolder
from apps.users.models import User


class PermissionsSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Permission
        fields = (
            'id',
            'name',
        )


class UserGroupSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Group
        fields = (
            'id',
            'name',
        )


class GroupSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        expandable_fields = {
            'permissions': (PermissionsSerializer, {'many': True}),
        }


class GeneralUserSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
        extra_kwargs = {
            'date_joined': {'read_only': True},
            'last_login': {'read_only': True},
        }
        ref_name = 'GeneralUserSerializer'


class UserDetailSerializer(
    ConvertNoneToStringSerializerMixin, FlexFieldsModelSerializer
):
    ticket_holder_data = SerializerMethodField()

    class Meta:
        model = User
        exclude = ('password', 'username')
        none_to_str_fields = ('last_login',)
        ref_name = 'UserDetailSerializer'
        expandable_fields = {
            'user_permissions': (PermissionsSerializer, {'many': True}),
            'groups': (UserGroupSerializer, {'many': True}),
        }

    @staticmethod
    def get_ticket_holder_data(obj):
        try:
            ticket_holder = TicketHolder.objects.get(user=obj)
            return {
                'phone': ticket_holder.phone,
                'address': ticket_holder.address,
                'tickets_data': ticket_holder.tickets_data,
                'date_created': ticket_holder.date_created,
                'is_verified': ticket_holder.is_verified,
            }
        except TicketHolder.DoesNotExist:
            return {}


class UserListSerializer(ConvertNoneToStringSerializerMixin, FlexFieldsModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
        none_to_str_fields = ('last_login', 'role', 'team', 'last_opened', 'email')
        ref_name = 'UserListSerializer'
        expandable_fields = {
            'user_permissions': (PermissionsSerializer, {'many': True}),
            'groups': (UserGroupSerializer, {'many': True}),
        }


class UserCreateSerializer(FlexFieldsModelSerializer):
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserCreateSerializer, self).create(validated_data)

    class Meta:
        model = User
        exclude = (
            'date_joined',
            'last_login',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }
        ref_name = 'UserCreateSerializer'


class DjoserUserSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'groups', 'user_permissions')
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'read_only': True},
            'last_login': {'read_only': True},
            'date_joined': {'read_only': True},
            'is_superuser': {'read_only': True},
            'is_staff': {'read_only': True},
            'is_active': {'read_only': True},
            'role': {'read_only': True},
            'team': {'read_only': True},
        }
        ref_name = 'DjoserUserSerializer'

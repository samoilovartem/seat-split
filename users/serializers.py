from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission
from django.db.models import Q
from rest_framework import serializers

from users.models import User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class GeneralUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password', 'role', 'team')
        extra_kwargs = {
            'date_joined': {'read_only': True},
            'last_login': {'read_only': True},
        }
        ref_name = 'GeneralUserSerializer'


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
        ref_name = 'UserDetailSerializer'


class UserListSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    user_permissions = serializers.SerializerMethodField()

    def get_user_permissions(self, obj):
        if obj.is_superuser:
            all_permissions = Permission.objects.all().order_by('id').values('id', 'name', 'codename')
            return all_permissions
        user_permissions = Permission.objects.filter(
            Q(user=obj.id) | Q(group__user=obj.id)
        ).order_by('id').values('id', 'name', 'codename')
        return user_permissions

    class Meta:
        model = User
        exclude = ('password', 'role', 'team')
        ref_name = 'UserListSerializer'


class UserCreateSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserCreateSerializer, self).create(validated_data)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'groups',
                  'is_active', 'is_staff', 'is_superuser')
        ref_name = 'UserCreateSerializer'

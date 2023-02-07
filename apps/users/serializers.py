from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from rest_flex_fields import FlexFieldsModelSerializer

from apps.serializers import ConvertNoneToStringSerializerMixin
from apps.users.models import User


class GroupSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


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
    class Meta:
        model = User
        exclude = ('password',)
        none_to_str_fields = ('last_login', 'role', 'team', 'last_opened', 'email')
        ref_name = 'UserDetailSerializer'


class UserListSerializer(ConvertNoneToStringSerializerMixin, FlexFieldsModelSerializer):
    # groups = GroupSerializer(many=True, read_only=True)

    # -------- IF WE EVER NEED TO SHOW USER PERMISSIONS --------
    # user_permissions = serializers.SerializerMethodField()
    # def get_user_permissions(self, obj):
    #     if obj.is_superuser:
    #         all_permissions = Permission.objects.all()\
    #             .order_by('id')\
    #             .values('id', 'name', 'codename')
    #         return all_permissions
    #     user_permissions = Permission.objects.filter(
    #         Q(user=obj.id) | Q(group__user=obj.id)
    #     ).order_by('id').values('id', 'name', 'codename')
    #     return user_permissions

    class Meta:
        model = User
        exclude = ('password', 'groups', 'user_permissions')
        none_to_str_fields = ('last_login', 'role', 'team', 'last_opened', 'email')
        ref_name = 'UserListSerializer'


class UserCreateSerializer(FlexFieldsModelSerializer):
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserCreateSerializer, self).create(validated_data)

    class Meta:
        model = User
        exclude = (
            'date_joined',
            'last_login',
            'email',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }
        ref_name = 'UserCreateSerializer'

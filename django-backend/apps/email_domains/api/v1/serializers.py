from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from apps.email_domains.models import EmailDomains
from apps.serializers import UserSerializer
from apps.users.models import User


class EmailDomainsSerializer(FlexFieldsModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=User.objects.all()
    )

    class Meta:
        model = EmailDomains
        fields = '__all__'
        expandable_fields = {
            'created_by': UserSerializer,
        }

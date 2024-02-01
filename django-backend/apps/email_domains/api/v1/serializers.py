from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from django.contrib.auth import get_user_model

from apps.email_domains.models import EmailDomains
from apps.serializers import UserSerializer

User = get_user_model()


class EmailDomainsSerializer(FlexFieldsModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=False, queryset=User.objects.all())

    class Meta:
        model = EmailDomains
        fields = '__all__'
        expandable_fields = {
            'created_by': UserSerializer,
        }

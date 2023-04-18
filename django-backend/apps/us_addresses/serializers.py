from rest_framework import serializers

from apps.us_addresses.models import USAddresses


class USAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = USAddresses
        exclude = ('updated_at', 'created_at', 'location')

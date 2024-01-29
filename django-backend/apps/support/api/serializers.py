from rest_framework import serializers

from apps.support.models import Inquiry


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = '__all__'

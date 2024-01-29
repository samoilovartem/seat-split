from apps.support.models import Inquiry
from rest_framework import serializers


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = '__all__'

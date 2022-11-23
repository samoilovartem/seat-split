from rest_framework import serializers

from .models import MLBSoldInventory


class MLBSoldInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MLBSoldInventory
        fields = '__all__'

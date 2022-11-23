from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey

from sold_inventory.models import MLBSoldInventory
from sold_inventory.pagination import MLBSoldInventoryApiListPagination
from sold_inventory.serializers import MLBSoldInventorySerializer


class MLBSoldInventoryViewSet(viewsets.ModelViewSet):
    queryset = MLBSoldInventory.objects.all()
    serializer_class = MLBSoldInventorySerializer
    pagination_class = MLBSoldInventoryApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]
    my_tags = ["MLB Sold Inventory"]


class MLBSoldInventoryUniversalFilterViewSet(viewsets.ModelViewSet):
    serializer_class = MLBSoldInventorySerializer
    pagination_class = MLBSoldInventoryApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]
    my_tags = ["MLB Sold Inventory universal filter"]

    def get_queryset(self):
        filter_name = self.request.query_params.get('filter_name')
        value = self.request.query_params.get('value')
        return MLBSoldInventory.objects.filter(**{f"{filter_name}__icontains": value})

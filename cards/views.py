from rest_framework import viewsets
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import IsAuthenticated

from accounts.models import Accounts
from .filters import CardsFilterSet
from .serializers import CardsSerializer
from .pagination import CardsApiListPagination

from .models import Cards


class AllCardsViewSet(viewsets.ModelViewSet):
    queryset = Cards.objects.all()
    serializer_class = CardsSerializer
    pagination_class = CardsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]
    filterset_fields = '__all__'
    # filterset_class = CardsFilterSet
    my_tags = ["All cards"]


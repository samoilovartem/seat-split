from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import IsAuthenticated

from .filters import CardsFilterSet
from .serializers import CardsSerializer
from .pagination import CardsApiListPagination

from .models import Cards
from .utils import cards_per_value


class AllCardsViewSet(viewsets.ModelViewSet):
    queryset = Cards.objects.all()
    serializer_class = CardsSerializer
    pagination_class = CardsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]
    filterset_fields = '__all__'
    # filterset_class = CardsFilterSet
    my_tags = ["All cards"]

    @action(methods=['GET'], detail=False)
    def show_duplicates(self, request):
        duplicates = Cards.objects.values('account_assigned').annotate(Count('id')).order_by().filter(id__count__gt=1)
        return Response({'results': duplicates})

    @action(methods=['GET'], detail=False)
    def get_cards_per_team(self, request):
        result = cards_per_value('team')
        return Response({'results': result})

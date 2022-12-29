from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from cards.filters import CardsFilterSet
from cards.serializers import CardsSerializer
from cards.pagination import CardsApiListPagination
from cards.models import Cards
from cards.utils import cards_per_value


class AllCardsViewSet(viewsets.ModelViewSet):
    queryset = Cards.objects.all()
    serializer_class = CardsSerializer
    pagination_class = CardsApiListPagination
    filterset_class = CardsFilterSet
    search_fields = ['account_assigned', 'type', 'platform', 'parent_card', 'team', 'created_by__username',
                     'created_at']
    ordering_fields = ['id', 'account_assigned', 'type', 'platform', 'parent_card', 'team', 'created_by',
                       'created_at']
    my_tags = ["All cards"]

    @action(methods=['GET'], detail=False)
    def show_duplicates(self, request):
        duplicates = Cards.objects.values('account_assigned').annotate(Count('id')).order_by().filter(id__count__gt=1)
        return Response({'results': duplicates})

    @action(methods=['GET'], detail=False)
    def get_cards_per_team(self, request):
        result = cards_per_value('team')
        return Response({'results': result})

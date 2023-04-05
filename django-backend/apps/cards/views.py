from rest_flex_fields import FlexFieldsModelViewSet, is_expanded
from rest_framework.decorators import action
from rest_framework.response import Response

from django.db.models import Count, Prefetch

from apps.cards.filters import CardsFilterSet
from apps.cards.models import Cards
from apps.cards.serializers import CardsSerializer
from apps.users.models import User
from apps.utils import records_per_value


class AllCardsViewSet(FlexFieldsModelViewSet):
    def get_queryset(self):
        queryset = Cards.objects.all()
        if is_expanded(self.request, 'created_by'):
            queryset = queryset.prefetch_related(
                Prefetch('created_by', queryset=User.objects.only('id', 'username'))
            )
        return queryset

    permit_list_expands = ['created_by']
    serializer_class = CardsSerializer
    filterset_class = CardsFilterSet
    search_fields = [
        'account_assigned',
        'type',
        'platform',
        'parent_card',
        'team',
        'created_by__username',
        'created_at',
    ]
    ordering_fields = [
        'id',
        'account_assigned',
        'type',
        'platform',
        'parent_card',
        'team',
        'created_by',
        'created_at',
    ]
    my_tags = ['All cards']

    @action(methods=['GET'], detail=False)
    def show_duplicates(self, request):
        duplicates = (
            Cards.objects.values('account_assigned')
            .annotate(Count('id'))
            .order_by()
            .filter(id__count__gt=1)
        )
        return Response({'results': duplicates})

    @action(methods=['GET'], detail=False)
    def get_cards_per_team(self, request):
        result = records_per_value(Cards, 'team')
        return Response({'results': result})

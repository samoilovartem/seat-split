from rest_flex_fields import FlexFieldsModelViewSet, is_expanded
from rest_framework.decorators import action
from rest_framework.response import Response

from django.db.models import Prefetch

from apps.cards.filters import CardsFilterSet
from apps.cards.models import Cards
from apps.cards.serializers import CardsSerializer
from apps.common_services.duplicate_checker import DuplicateChecker
from apps.common_services.utils import records_per_value
from apps.users.models import User


class AllCardsViewSet(FlexFieldsModelViewSet):
    def get_queryset(self):
        queryset = Cards.objects.all()
        if is_expanded(self.request, "created_by"):
            queryset = queryset.prefetch_related(
                Prefetch("created_by", queryset=User.objects.only("id", "username"))
            )
        return queryset

    permit_list_expands = ["created_by"]
    serializer_class = CardsSerializer
    filterset_class = CardsFilterSet
    search_fields = [
        "account_assigned",
        "type",
        "platform",
        "parent_card",
    ]
    ordering_fields = [
        "id",
        "account_assigned",
        "team",
        "created_by",
        "created_at",
    ]
    my_tags = ["All cards"]

    @action(methods=["GET"], detail=False)
    def show_duplicates(self, request):
        duplicate_checker = DuplicateChecker(model=Cards, field="account_assigned")
        return duplicate_checker.get_duplicate_summary()

    @action(methods=["GET"], detail=False)
    def get_cards_per_team(self, request):
        result = records_per_value(Cards, "team")
        return Response({"results": result})

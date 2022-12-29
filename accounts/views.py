from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.filters import AccountsFilterSet
from accounts.models import Accounts
from accounts.pagination import AccountsApiListPagination
from accounts.serializers import AccountsSerializer
from accounts.utils import accounts_per_value


class AllAccountsViewSet(viewsets.ModelViewSet):
    queryset = Accounts.objects.all()
    serializer_class = AccountsSerializer
    pagination_class = AccountsApiListPagination
    filterset_class = AccountsFilterSet
    search_fields = ['email', 'type', 'created_by__username', 'first_name', 'last_name']
    ordering_fields = ['id', 'email', 'type', 'created_by', 'first_name', 'last_name', 'created_at',
                       'recovery_email', 'ld_computer_used', 'last_opened', 'disabled']
    my_tags = ["All accounts"]

    @action(methods=['GET'], detail=False)
    def show_duplicates(self, request):
        duplicates = Accounts.objects.values('email').annotate(Count('id')).order_by().filter(id__count__gt=1)
        return Response({'results': duplicates})

    @action(methods=['GET'], detail=False)
    def get_accounts_per_type(self, request):
        result = accounts_per_value('type')
        return Response({'results': result})

    @action(methods=['GET'], detail=False)
    def get_accounts_per_team(self, request):
        result = accounts_per_value('team')
        return Response({'results': result})

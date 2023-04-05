from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django.db.models import Count

from apps.accounts.filters import AccountsFilterSet
from apps.accounts.models import Accounts
from apps.accounts.serializers import AccountsSerializer
from apps.accounts.utils import AccountsCSVExporter, AccountsCSVImporter
from apps.utils import records_per_value


class AllAccountsViewSet(ModelViewSet):
    queryset = Accounts.objects.all()
    serializer_class = AccountsSerializer
    filterset_class = AccountsFilterSet
    search_fields = [
        'email',
        'first_name',
        'last_name',
        'comments',
    ]
    ordering_fields = [
        'id',
        'type',
        'created_by',
        'created_at',
        'ld_computer_used',
        'last_opened',
        'disabled',
    ]
    my_tags = ['All accounts']

    @action(methods=['GET'], detail=False)
    def show_duplicates(self, request):
        duplicates = (
            Accounts.objects.values('email')
            .annotate(duplicates=Count('id'))
            .order_by()
            .filter(duplicates__gt=1)
        )
        unique_accounts_number = Accounts.objects.values('email').distinct().count()
        unique_duplicates_number = duplicates.count()
        return Response(
            {
                'total number of accounts': unique_duplicates_number
                + unique_accounts_number,
                'total number of unique duplicate accounts': unique_duplicates_number,
                'total number of unique accounts': unique_accounts_number,
                'all duplicate accounts': duplicates,
            }
        )

    @action(methods=['GET'], detail=False)
    def get_accounts_per_type(self, request):
        result = records_per_value(Accounts, 'type')
        return Response({'results': result})

    @action(methods=['GET'], detail=False)
    def get_accounts_per_team(self, request):
        result = records_per_value(Accounts, 'team')
        return Response({'results': result})

    @action(methods=['POST'], detail=False)
    def import_file(self, request):
        importer = AccountsCSVImporter(request)
        return importer.import_file()

    @action(methods=['POST'], detail=False)
    def export_file(self, request):
        exporter = AccountsCSVExporter(request)
        return exporter.export_file()

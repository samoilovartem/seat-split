from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.accounts.filters import AccountsFilterSet
from apps.accounts.models import Accounts
from apps.accounts.resource import AccountsResource
from apps.accounts.serializers import AccountsSerializer
from apps.utils.duplicate_checker import DuplicateChecker
from apps.utils.file_exporter import CSVExporter
from apps.utils.file_importer import CSVImporter
from apps.utils.utils import records_per_value


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
        duplicate_checker = DuplicateChecker(model=Accounts, field='email')
        return duplicate_checker.get_duplicate_summary()

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
        csv_importer = CSVImporter(
            request,
            app_name='accounts',
            model_name='Accounts',
            resource=AccountsResource,
            duplicate_check_column='email',
        )
        response = csv_importer.import_file()
        return response

    @action(methods=['POST'], detail=False)
    def export_file(self, request):
        csv_exporter = CSVExporter(request, app_name='accounts', model_name='Accounts')
        return csv_exporter.export_file()

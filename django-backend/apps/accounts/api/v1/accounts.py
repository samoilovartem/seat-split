from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.accounts.api.v1.filters import AccountsFilterSet
from apps.accounts.api.v1.serializers import AccountsSerializer
from apps.accounts.models import Accounts
from apps.accounts.resource import AccountsResource
from apps.common_services.csv_normalizer import apply_request_fields
from apps.common_services.duplicate_checker import DuplicateChecker
from apps.common_services.file_exporter import CSVExporter
from apps.common_services.file_importer import CSVImporter
from apps.common_services.utils import records_per_value
from apps.config import AccountsCSVConfig

APP_NAME = Accounts._meta.app_label
MODEL_NAME = Accounts._meta.model_name


class AllAccountsViewSet(ModelViewSet):
    queryset = Accounts.objects.all()
    serializer_class = AccountsSerializer
    filterset_class = AccountsFilterSet
    search_fields = [
        'email',
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
    csv_config = AccountsCSVConfig()
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
            app_name=APP_NAME,
            model_name=MODEL_NAME,
            resource=AccountsResource,
            duplicate_check_column=self.csv_config.duplicate_check_column,
            exclude_fields=self.csv_config.exclude_fields,
        )
        response = csv_importer.import_file()
        return response

    @action(methods=['POST'], detail=False)
    def export_file(self, request):
        csv_exporter = CSVExporter(request, app_name=APP_NAME, model_name=MODEL_NAME)
        return csv_exporter.export_file()

    @action(methods=['POST'], detail=False)
    def flexible_import_csv(self, request):
        response = apply_request_fields(
            request,
            app_name=APP_NAME,
            model_name=MODEL_NAME,
            exclude_fields=self.csv_config.exclude_fields,
            strict_fields=self.csv_config.strict_fields,
        )
        return response

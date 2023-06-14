from apps.common_services.csv_normalizer import (
    apply_request_fields,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.accounts.filters import AccountsFilterSet
from apps.accounts.models import Accounts
from apps.accounts.resource import AccountsResource
from apps.accounts.serializers import AccountsSerializer
from apps.common_services.duplicate_checker import DuplicateChecker
from apps.common_services.file_exporter import CSVExporter
from apps.common_services.file_importer import CSVImporter
from apps.common_services.utils import (
    records_per_value,
)


class AllAccountsViewSet(ModelViewSet):
    queryset = Accounts.objects.all()
    serializer_class = AccountsSerializer
    filterset_class = AccountsFilterSet
    search_fields = [
        "email",
        "comments",
    ]
    ordering_fields = [
        "id",
        "type",
        "created_by",
        "created_at",
        "ld_computer_used",
        "last_opened",
        "disabled",
    ]
    my_tags = ["All accounts"]

    @action(methods=["GET"], detail=False)
    def show_duplicates(self, request):
        duplicate_checker = DuplicateChecker(model=Accounts, field="email")
        return duplicate_checker.get_duplicate_summary()

    @action(methods=["GET"], detail=False)
    def get_accounts_per_type(self, request):
        result = records_per_value(Accounts, "type")
        return Response({"results": result})

    @action(methods=["GET"], detail=False)
    def get_accounts_per_team(self, request):
        result = records_per_value(Accounts, "team")
        return Response({"results": result})

    @action(methods=["POST"], detail=False)
    def import_file(self, request):
        csv_importer = CSVImporter(
            request,
            app_name="accounts",
            model_name="Accounts",
            resource=AccountsResource,
            duplicate_check_column="email",
            exclude_fields=["updated_at", "id"],
        )
        response = csv_importer.import_file()
        return response

    @action(methods=["POST"], detail=False)
    def export_file(self, request):
        csv_exporter = CSVExporter(request, app_name="accounts", model_name="Accounts")
        return csv_exporter.export_file()

    @action(methods=["POST"], detail=False)
    def flexible_import_csv(self, request):
        new_request = apply_request_fields(
            request,
            "accounts",
            "Accounts",
            exclude_fields=["updated_at", "id"],
        )

        csv_importer = CSVImporter(
            new_request,
            app_name="accounts",
            model_name="Accounts",
            resource=AccountsResource,
            duplicate_check_column="email",
            exclude_fields=["updated_at", "id"],
        )

        response = csv_importer.import_file()
        return response

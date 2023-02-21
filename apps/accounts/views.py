from django.db.models import Count
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from tablib import Dataset

from apps.accounts.filters import AccountsFilterSet
from apps.accounts.models import Accounts
from apps.accounts.resource import AccountsResource
from apps.accounts.serializers import AccountsSerializer
from apps.accounts.utils import accounts_per_value


class AllAccountsViewSet(ModelViewSet):
    queryset = Accounts.objects.all()
    serializer_class = AccountsSerializer
    filterset_class = AccountsFilterSet
    search_fields = [
        'email',
        'type',
        'created_by',
        'first_name',
        'last_name',
        'comments',
    ]
    ordering_fields = [
        'id',
        'email',
        'type',
        'created_by',
        'first_name',
        'last_name',
        'created_at',
        'recovery_email',
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
        unique_duplicates_number = len(duplicates)
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
        result = accounts_per_value('type')
        return Response({'results': result})

    @action(methods=['GET'], detail=False)
    def get_accounts_per_team(self, request):
        result = accounts_per_value('team')
        return Response({'results': result})

    @action(methods=['POST'], detail=False)
    def import_csv(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'success': False, 'error': 'No file was uploaded.'})

        resource = AccountsResource()
        dataset = Dataset().load(file.read().decode('utf-8'), format='csv')
        dry_run_result = resource.import_data(dataset, dry_run=True)

        if dry_run_result.has_validation_errors():
            invalid_rows = dry_run_result.invalid_rows
            error_messages = []
            for invalid_row in invalid_rows:
                email = invalid_row.values[3]
                error_messages.append(f'Errors in email "{email}": {invalid_row.error}')
            return Response({'success': False, 'errors': error_messages})

        elif dry_run_result.has_errors():
            return Response({'success': False, 'errors': dry_run_result.row_errors()})

        else:
            resource.import_data(dataset, dry_run=False)
            return Response({'success': True, 'message': 'Data uploaded successfully.'})

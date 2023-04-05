from csv import DictWriter
from io import StringIO

from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from tablib import Dataset, UnsupportedFormat

from django.http import HttpResponse

from apps.accounts.models import Accounts
from apps.accounts.resource import AccountsResource
from apps.utils import get_model_fields


class AccountsCSVImporter:
    def __init__(self, request):
        self.request = request
        self.file = request.FILES.get('file')

    def import_file(self):
        if not self.file:
            return Response({'success': False, 'error': 'No file was uploaded.'})

        try:
            dataset = self._load_dataset_from_file()
        except UnsupportedFormat:
            return Response({'success': False, 'error': 'Unsupported file format.'})

        expected_columns = get_model_fields(app_name='accounts', model_name='Accounts')
        csv_columns = dataset.headers
        missing_columns = set(expected_columns) - set(csv_columns)

        if missing_columns:
            error_message = f'CSV file is missing the following columns: {", ".join(missing_columns)}'
            return Response({'success': False, 'error': error_message})

        email_column = csv_columns.index('email')
        existing_emails = self._get_existing_emails(email_column, dataset)

        if existing_emails:
            return Response({'success': False, 'errors': existing_emails})

        resource = AccountsResource()
        result = resource.import_data(dataset, dry_run=True)

        if result.has_validation_errors():
            invalid_rows = result.invalid_rows
            error_messages = self._get_validation_errors(invalid_rows)
            return Response({'success': False, 'errors': error_messages})

        elif result.has_errors():
            return Response({'success': False, 'errors': result.row_errors()})

        else:
            resource.import_data(dataset, dry_run=False)
            return Response({'success': True, 'message': 'Data uploaded successfully.'})

    @staticmethod
    def _get_existing_emails(email_column, dataset):
        emails = [row[email_column] for row in dataset]
        existing_emails = Accounts.objects.filter(email__in=emails).values_list(
            'email', flat=True
        )
        error_messages = [
            f'Email {email} already exists in the database.'
            for email in existing_emails
        ]
        return error_messages

    @staticmethod
    def _get_validation_errors(email_column, invalid_rows):
        error_messages = []
        for invalid_row in invalid_rows:
            email = invalid_row.values[email_column + 1]
            error_messages.append(
                f'Errors in email {email}. Columns: {invalid_row.error}'
            )
        return error_messages

    def _load_dataset_from_file(self):
        if self.file.name.endswith('.xlsx'):
            dataset = Dataset().load(self.file.read(), format='xlsx')
        elif self.file.name.endswith('.csv'):
            dataset = Dataset().load(self.file.read().decode('utf-8'), format='csv')
        else:
            raise UnsupportedFormat('Unsupported file format.')
        return dataset


class AccountsCSVExporter:
    def __init__(self, request):
        self.request = request
        self.exclude_fields = request.data.get('exclude_fields', [])
        self.include_fields = request.data.get('fields', None)
        self.all_fields = get_model_fields(app_name='accounts', model_name='Accounts')

    def export_file(self):
        invalid_exclude_fields = self._get_invalid_fields(self.exclude_fields)
        if invalid_exclude_fields:
            return self._error_response(
                'Invalid exclude_field(s)', invalid_exclude_fields
            )

        if self.include_fields:
            invalid_include_fields = self._get_invalid_fields(self.include_fields)
            if invalid_include_fields:
                return self._error_response('Invalid field(s)', invalid_include_fields)
            dataset_headers = self.include_fields
        else:
            dataset_headers = get_model_fields(
                app_name='accounts',
                model_name='Accounts',
                exclude_fields=self.exclude_fields,
            )

        csv_data = self._generate_csv(dataset_headers)

        return self._csv_http_response(csv_data, "accounts.csv")

    def _get_invalid_fields(self, fields):
        return set(fields) - set(self.all_fields)

    @staticmethod
    def _error_response(message, invalid_fields):
        return Response(
            {
                'success': False,
                'error': f'{message}: {", ".join(invalid_fields)}',
            },
            status=HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def _generate_csv(dataset_headers):
        output = StringIO()
        writer = DictWriter(output, fieldnames=dataset_headers)

        writer.writeheader()

        accounts = Accounts.objects.values(*dataset_headers).order_by('id').iterator()
        for account in accounts:
            writer.writerow(account)

        return output.getvalue()

    @staticmethod
    def _csv_http_response(csv_data, filename):
        response = HttpResponse(csv_data, content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response

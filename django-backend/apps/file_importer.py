from rest_framework.response import Response
from tablib import Dataset, UnsupportedFormat

from django.apps import apps

from apps.utils import get_model_fields


class CSVImporter:
    def __init__(self, request, app_name, model_name, resource, duplicate_check_column):
        self.request = request
        self.file = request.FILES.get('file')
        self.app_name = app_name
        self.model_name = model_name
        self.model = apps.get_model(app_label=app_name, model_name=model_name)
        self.resource = resource
        self.duplicate_check_column = duplicate_check_column

    def import_file(self):
        if not self.file:
            return Response({'success': False, 'error': 'No file was uploaded.'})

        try:
            dataset = self._load_dataset_from_file()
        except UnsupportedFormat:
            return Response({'success': False, 'error': 'Unsupported file format.'})

        expected_columns = get_model_fields(
            app_name=self.app_name,
            model_name=self.model_name,
            exclude_fields=['updated_at'],
        )
        csv_columns = dataset.headers
        missing_columns = set(expected_columns) - set(csv_columns)

        if missing_columns:
            error_message = f'CSV file is missing the following columns: {", ".join(missing_columns)}'
            return Response({'success': False, 'error': error_message})

        duplicate_check_column_index = csv_columns.index(self.duplicate_check_column)
        existing_records = self._get_existing_records(
            duplicate_check_column_index, dataset
        )

        if existing_records:
            return Response({'success': False, 'errors': existing_records})

        resource_instance = self.resource()
        result = resource_instance.import_data(dataset, dry_run=True)

        if result.has_validation_errors():
            invalid_rows = result.invalid_rows
            error_messages = self._get_validation_errors(
                duplicate_check_column_index, invalid_rows
            )
            return Response({'success': False, 'errors': error_messages})

        elif result.has_errors():
            return Response({'success': False, 'errors': result.row_errors()})

        else:
            resource_instance.import_data(dataset, dry_run=False)
            return Response({'success': True, 'message': 'Data uploaded successfully.'})

    def _get_existing_records(self, duplicate_check_column_index, dataset):
        duplicate_check_values = [row[duplicate_check_column_index] for row in dataset]
        existing_records = self.model.objects.filter(
            **{f"{self.duplicate_check_column}__in": duplicate_check_values}
        ).values_list(self.duplicate_check_column, flat=True)
        unique_existing_records = set(existing_records)
        error_messages = [
            f'{self.duplicate_check_column.capitalize()} {value} already exists in the database.'
            for value in unique_existing_records
        ]
        return error_messages

    def _get_validation_errors(self, duplicate_check_column_index, invalid_rows):
        error_messages = []
        for invalid_row in invalid_rows:
            duplicate_check_value = invalid_row.values[duplicate_check_column_index + 1]
            error_messages.append(
                f'Errors in {self.duplicate_check_column} {duplicate_check_value}. Columns: {invalid_row.error}'
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

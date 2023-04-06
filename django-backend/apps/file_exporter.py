from csv import DictWriter
from io import StringIO

from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from django.apps import apps
from django.http import HttpResponse


class CSVExporter:
    def __init__(self, request, app_name, model_name):
        self.request = request
        self.app_name = app_name
        self.model_name = model_name
        self.exclude_fields = request.data.get('exclude_fields', [])
        self.include_fields = request.data.get('fields', None)
        self.all_fields = self.get_model_fields(app_name, model_name)

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
            dataset_headers = self.get_model_fields(
                self.app_name,
                self.model_name,
                exclude_fields=self.exclude_fields,
            )
        csv_data = self._generate_csv(dataset_headers)

        return self._csv_http_response(csv_data, f'{self.model_name.lower()}.csv')

    def _get_invalid_fields(self, fields):
        return set(fields) - set(self.all_fields)

    @staticmethod
    def get_model_fields(app_name, model_name, exclude_fields=None):
        model = apps.get_model(app_name, model_name)
        fields = [field.name for field in model._meta.fields]

        if exclude_fields:
            return [field for field in fields if field not in exclude_fields]
        return fields

    @staticmethod
    def _error_response(message, invalid_fields):
        return Response(
            {
                'success': False,
                'error': f'{message}: {", ".join(invalid_fields)}',
            },
            status=HTTP_400_BAD_REQUEST,
        )

    def _generate_csv(self, dataset_headers):
        output = StringIO()
        writer = DictWriter(output, fieldnames=dataset_headers)

        writer.writeheader()

        model = apps.get_model(self.app_name, self.model_name)
        records = model.objects.values(*dataset_headers).order_by('id').iterator()
        for record in records:
            writer.writerow(record)

        return output.getvalue()

    @staticmethod
    def _csv_http_response(csv_data, filename):
        response = HttpResponse(csv_data, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

from csv import DictWriter
from io import StringIO

from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from django.apps import apps
from django.http import HttpResponse


class CSVExporter:
    """
    CSVExporter is a utility class for exporting data from a Django model to a CSV file.

    Attributes:
        request: Django HttpRequest object.
        app_name: String representing Django app name where the model is located.
        model_name: String representing Django model name whose data will be exported.
        exclude_fields: List of fields to exclude from the export.
        include_fields: List of fields to include in the export.
        all_fields: List of all fields in the model.
    """

    def __init__(self, request, app_name, model_name):
        self.request = request
        self.app_name = app_name
        self.model_name = model_name
        self.exclude_fields = request.data.get('exclude_fields', [])
        self.include_fields = request.data.get('fields', None)
        self.all_fields = self.get_model_fields(app_name, model_name)

    def export_file(self):
        """
        Export data from the specified Django model to a CSV file.

        Returns:
            Django Rest Framework Response object with a link to the CSV file, or an error message.
        """
        invalid_exclude_fields = self._get_invalid_fields(self.exclude_fields)
        if invalid_exclude_fields:
            return self._error_response('Invalid exclude_field(s)', invalid_exclude_fields)

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
        """
        Retrieve invalid fields that are not in the model.

        Returns:
            Set of invalid fields.
        """
        return set(fields) - set(self.all_fields)

    @staticmethod
    def get_model_fields(app_name, model_name, exclude_fields=None):
        """
        Retrieve fields of the model.

        If exclude_fields is provided, fields in that list will be excluded.

        Returns:
            List of fields in the model.
        """
        model = apps.get_model(app_name, model_name)
        fields = [field.name for field in model._meta.fields]

        if exclude_fields:
            return [field for field in fields if field not in exclude_fields]
        return fields

    @staticmethod
    def _error_response(message, invalid_fields):
        """
        Construct an error response with the provided message and invalid fields.

        Returns:
            Django Rest Framework Response object containing an error message.
        """
        return Response(
            {
                'success': False,
                'error': f'{message}: {", ".join(invalid_fields)}',
            },
            status=HTTP_400_BAD_REQUEST,
        )

    def _generate_csv(self, dataset_headers):
        """
        Generate a CSV file from the data in the model using the provided dataset headers.

        Returns:
            String representation of the CSV data.
        """
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
        """
        Construct a HttpResponse object for the generated CSV file.

        Returns:
            Django HttpResponse object with the CSV file attached.
        """
        response = HttpResponse(csv_data, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

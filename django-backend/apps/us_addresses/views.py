from import_export.resources import modelresource_factory
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.viewsets import GenericViewSet

from apps.us_addresses.models import USAddresses
from apps.us_addresses.serializers import USAddressSerializer
from apps.us_addresses.utils import AddressesWithinDistanceHandler
from apps.utils.file_importer import CSVImporter


class AddressesWithinDistanceViewSet(GenericViewSet, ListAPIView):
    queryset = USAddresses.objects.all()
    serializer_class = USAddressSerializer
    my_tags = ['US addresses within a distance']

    def list(self, request, *args, **kwargs):
        coordinates = request.query_params.get('coordinates')
        distance = request.query_params.get('distance')
        random = request.query_params.get('random', 'false').lower() == 'true'

        if coordinates is None or distance is None:
            return Response(
                {'error': 'coordinates and distance are required fields'},
                status=HTTP_400_BAD_REQUEST,
            )

        try:
            handler = AddressesWithinDistanceHandler(
                self, coordinates, distance, random
            )
            return handler.handle_request()
        except ValueError as e:
            return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['POST'], detail=False)
    def import_file(self, request):
        csv_importer = CSVImporter(
            request,
            app_name='us_addresses',
            model_name='USAddresses',
            resource=modelresource_factory(USAddresses),
            exclude_fields=['updated_at', 'created_at', 'id', 'location', 'is_used'],
        )
        response = csv_importer.import_file()
        return response

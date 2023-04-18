from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.viewsets import GenericViewSet

from apps.us_addresses.models import USAddresses
from apps.us_addresses.serializers import USAddressSerializer
from apps.us_addresses.utils import AddressesWithinDistanceHandler


class AddressesWithinDistanceViewSet(GenericViewSet, ListAPIView):
    queryset = USAddresses.objects.all()
    serializer_class = USAddressSerializer

    def list(self, request, *args, **kwargs):
        coordinates = request.query_params.get('coordinates')
        distance = request.query_params.get('distance')
        random = request.query_params.get('random', 'false').lower() == 'true'

        if coordinates is None or distance is None:
            return Response(
                {'error': 'coordinates and distance are required fields'},
                status=HTTP_400_BAD_REQUEST,
            )

        handler = AddressesWithinDistanceHandler(self, coordinates, distance, random)

        try:
            return handler.handle_request()
        except Exception as e:
            return Response({'error': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

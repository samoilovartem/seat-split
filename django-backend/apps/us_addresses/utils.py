from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry

from apps.us_addresses.models import USAddresses


class AddressesWithinDistanceHandler:
    def __init__(self, view, coordinates: str, distance: float, random: bool):
        self.view = view
        self.point = self.parse_coordinates(coordinates)
        self.distance = distance
        self.random = random

    @staticmethod
    def parse_coordinates(coordinates: str) -> GEOSGeometry:
        try:
            coordinates_list = [
                float(coord.strip()) for coord in coordinates.split(',')
            ]
            if len(coordinates_list) != 2:
                raise ValueError(
                    'Invalid coordinates input. Expected format: "longitude,latitude"'
                )
            return GEOSGeometry(
                f'POINT({coordinates_list[0]} {coordinates_list[1]})', srid=4326
            )
        except ValueError as e:
            raise ValueError(f'Error parsing coordinates: {str(e)}')

    def get_random_address(self) -> USAddresses:
        return (
            USAddresses.objects.filter(
                location__distance_lte=(self.point, self.distance)
            )
            .order_by('?')
            .first()
        )

    def get_paginated_addresses(self) -> Response:
        queryset = USAddresses.objects.filter(
            location__distance_lte=(self.point, self.distance)
        ).annotate(distance=Distance('location', self.point))
        queryset = self.view.filter_queryset(queryset)
        page = self.view.paginate_queryset(queryset)
        if page is not None:
            serializer = self.view.get_serializer(page, many=True)
            return self.view.get_paginated_response(serializer.data)

        serializer = self.view.get_serializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def handle_request(self) -> Response:
        try:
            if self.random:
                address = self.get_random_address()
                if address is None:
                    return Response(
                        {'error': 'No address found within specified distance'},
                        status=HTTP_404_NOT_FOUND,
                    )
                serializer = self.view.get_serializer(address)
                return Response(serializer.data, status=HTTP_200_OK)
            else:
                return self.get_paginated_addresses()
        except ValueError as e:
            return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)

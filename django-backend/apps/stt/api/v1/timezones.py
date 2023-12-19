from pytz import all_timezones
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class TimezoneListView(APIView):
    """Returns a list of all timezones."""

    def get(self, request, format=None):
        timezones = all_timezones
        response_data = {
            'meta': {
                'count': len(timezones),
            },
            'data': timezones,
        }
        return Response(response_data, status=status.HTTP_200_OK)

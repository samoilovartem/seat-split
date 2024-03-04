from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from config.components.business_related import SUPPORTED_LEAGUES


class LeagueListView(APIView):
    """Returns a list of all currently supported leagues."""

    def get(self, request):
        response_data = {
            'meta': {
                'count': len(SUPPORTED_LEAGUES),
            },
            'data': SUPPORTED_LEAGUES,
        }
        return Response(response_data, status=status.HTTP_200_OK)

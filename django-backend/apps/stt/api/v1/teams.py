from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.stt.api.v1.serializers import TeamSerializer
from apps.stt.models import Team
from config.components.business_related import SUPPORTED_LEAGUES


class TeamViewSet(ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filterset_fields = ['league', 'city', 'name']
    permission_classes = (IsAuthenticated,)

    my_tags = ['teams']

    @action(detail=False, methods=['get'])
    def get_teams_and_leagues_info(self, request):
        teams = Team.objects.all()
        team_serializer = TeamSerializer(teams, many=True)

        data = {'leagues': SUPPORTED_LEAGUES, 'teams': team_serializer.data}

        return Response(data)

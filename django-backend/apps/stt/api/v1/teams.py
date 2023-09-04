from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_api_key.permissions import HasAPIKey

from apps.stt.api.v1.serializers import TeamSerializer
from apps.stt.models import Team


class TeamViewSet(ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filterset_fields = ['league', 'city', 'name']
    permission_classes = [HasAPIKey]

    my_tags = ['all teams']

    @action(detail=False, methods=['get'])
    def get_teams_and_leagues_info(self, request):
        leagues = ['NFL', 'NBA', 'NHL', 'MLB', 'MLS']

        teams = Team.objects.all()
        team_serializer = TeamSerializer(teams, many=True)

        data = {'leagues': leagues, 'teams': team_serializer.data}

        return Response(data)

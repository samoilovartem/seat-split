from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.stt.api.v1.serializers import TeamSerializer
from apps.stt.models import Team


class TeamViewSet(ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filterset_fields = ['league', 'city', 'name']
    permission_classes = [AllowAny]

    my_tags = ['all teams']


class TeamsAndLeaguesInfoView(APIView):
    def get(self, request):
        leagues = ['NFL', 'NBA', 'NHL', 'MLB', 'MLS']

        teams = Team.objects.all()
        team_serializer = TeamSerializer(teams, many=True)

        data = {'leagues': leagues, 'teams': team_serializer.data}

        return Response(data)

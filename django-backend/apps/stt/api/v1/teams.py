from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.stt.api.serializers import TeamSerializer
from apps.stt.models import Team, TicketHolder
from config.components.business_related import SUPPORTED_LEAGUES


class TeamViewSet(ModelViewSet):
    queryset = Team.objects.all().order_by('id')
    serializer_class = TeamSerializer
    filterset_fields = ['league', 'city', 'name']
    permission_classes = (IsAuthenticated,)

    my_tags = ['teams']

    def get_queryset(self):
        queryset = super().get_queryset()

        user = self.request.user
        ticket_holder = TicketHolder.objects.filter(user=user).first()

        if ticket_holder:
            associated_teams = ticket_holder.ticket_holder_teams.values_list(
                'team', flat=True
            )
            queryset = queryset.exclude(id__in=associated_teams)

        return queryset

    @action(detail=False, methods=['get'])
    def get_teams_and_leagues_info(self, request):
        teams = Team.objects.all()
        team_serializer = TeamSerializer(teams, many=True)

        data = {'leagues': SUPPORTED_LEAGUES, 'teams': team_serializer.data}

        return Response(data)

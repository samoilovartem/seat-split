from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from django.db.models import Prefetch

from apps.stt.models import TicketHolderTeam
from apps.users.api.v1.serializers import UserSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    my_tags = ['users']

    def get_queryset(self):
        queryset = (
            User.objects.select_related('ticket_holder_user')
            .prefetch_related(
                Prefetch(
                    lookup='ticket_holder_user__ticket_holder_teams',
                    queryset=TicketHolderTeam.objects.select_related('team'),
                )
            )
            .order_by('id')
        )
        if self.request.user.is_staff or self.request.user.is_superuser:
            return queryset
        return queryset.filter(pk=self.request.user.pk)

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def blacklist_jwt(request):
    """
    Is used to blacklist a refresh_token and logout a user.
    Ex.: /api/v1/users/blacklist_jwt/?refresh_token=<refresh_token>
    """
    try:
        refresh_token = request.data.get('refresh_token')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(data={'message': 'The token has been blacklisted'})
    except Exception as error:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': error})

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model, update_session_auth_hash
from django.db.models import Prefetch

from apps.stt.models import TicketHolderTeam
from apps.users.api.v1.serializers import ChangePasswordSerializer, UserSerializer

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

    @action(detail=False, methods=['GET'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    @action(detail=False, methods=['POST'])
    def change_password(self, request, pk=None):
        user = request.user
        serializer = ChangePasswordSerializer(
            data=request.data, context={'request': request}
        )

        if serializer.is_valid():
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {'old_password': ['Old password is incorrect.']},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(serializer.validated_data['new_password'])
            user.save()
            update_session_auth_hash(request, user)

            return Response({'status': 'password changed'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

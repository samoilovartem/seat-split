from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from apps.stt.models import TicketHolderTeam
from apps.stt.utils import invalidate_user_auth_token
from apps.users.api.serializers import (
    ChangePasswordSerializer,
    EmailChangeSerializer,
    PasswordResetRequestSerializer,
    UserSerializer,
)
from apps.users.tasks import send_email_change_confirmation, send_password_reset_email
from config.components.celery import CELERY_GENERAL_COUNTDOWN
from config.components.redis import redis_general_connection

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
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {'old_password': ['Old password is incorrect.']},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(serializer.validated_data['new_password'])
            user.save()
            invalidate_user_auth_token(user)

            return Response({'status': 'password changed'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=EmailChangeSerializer)
    @action(detail=False, methods=['POST'])
    def change_email(self, request, pk=None):
        serializer = EmailChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            new_email = serializer.validated_data['new_email']

            send_email_change_confirmation.apply_async(
                args=(new_email, user.id), countdown=CELERY_GENERAL_COUNTDOWN
            )

            key = f'email_change_{user.id}'
            redis_general_connection.setex(key, 86_400, new_email)  # 86,400 seconds = 24 hours

            return Response(
                {'message': 'Verification email sent to the new address.'},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=PasswordResetRequestSerializer)
    @action(detail=False, methods=['POST'], permission_classes=(AllowAny,))
    def reset_password(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                send_password_reset_email.apply_async(
                    args=(email, user.id), countdown=CELERY_GENERAL_COUNTDOWN
                )
            except User.DoesNotExist:
                pass

            return Response(
                {
                    'message': 'If your email is in our database, you will receive a link to reset your password.'
                },
                status=status.HTTP_200_OK,
            )

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

from uuid import UUID

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import password_validation
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from apps.stt.api.serializers import RegisterSerializer
from apps.stt.models import TicketHolder, User
from apps.stt.tasks import send_email_confirmation, send_email_confirmed
from apps.users.tasks import send_email_change_confirmed
from config.components.celery import CELERY_GENERAL_COOLDOWN
from config.components.redis import redis_connection


class RegisterView(APIView):
    permission_classes = (AllowAny,)
    my_tags = ['registration and verification']

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            try:
                password_validation.validate_password(password)
            except Exception as e:
                return Response(
                    {'password': list(e.messages)}, status=status.HTTP_400_BAD_REQUEST
                )

            user = User.objects.create_user(
                email=serializer.validated_data['email'],
                password=password,
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
            )

            TicketHolder.objects.create(
                user=user,
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                phone=serializer.validated_data['phone'],
                address=serializer.validated_data['address'],
                is_season_ticket_interest=serializer.validated_data[
                    'is_season_ticket_interest'
                ],
                is_card_interest=serializer.validated_data['is_card_interest'],
            )

            send_email_confirmation.apply_async(args=(user.email, user.id), countdown=5)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyView(APIView):
    permission_classes = (AllowAny,)
    my_tags = ['registration and verification']

    def post(self, request, *args, **kwargs):
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))

            try:
                user_id = UUID(uid)
            except ValueError:
                return Response(
                    {'error': 'Invalid user ID format.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = User.objects.get(pk=user_id)

            is_email_change_verification = False
            new_email = redis_connection.get(f'email_change_{uid}')

            if new_email:
                is_email_change_verification = True

            if default_token_generator.check_token(user, token):
                if not is_email_change_verification:
                    if user.is_verified:
                        return Response(
                            {'error': 'User already verified.'},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    user.is_verified = True
                    user.save()

                    send_email_confirmed.apply_async(
                        args=(user.email,), countdown=CELERY_GENERAL_COOLDOWN
                    )

                else:
                    user.email = new_email
                    user.username = new_email
                    user.save()

                    redis_connection.delete(f'email_change_{uid}')

                    send_email_change_confirmed.apply_async(
                        args=(new_email,), countdown=CELERY_GENERAL_COOLDOWN
                    )

                return Response(
                    {'message': 'Verification successful'}, status=status.HTTP_200_OK
                )

            else:
                return Response(
                    {'error': 'Token is not valid.'}, status=status.HTTP_400_BAD_REQUEST
                )
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {'error': 'Invalid link or user not found.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

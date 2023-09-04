from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import password_validation

from apps.stt.api.v1.serializers import RegisterSerializer
from apps.stt.models import TicketHolder, User


class RegisterView(APIView):
    permission_classes = (AllowAny,)

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

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

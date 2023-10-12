from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from django.core.exceptions import ObjectDoesNotExist

from apps.stt.api.v1.serializers import CustomTokenObtainPairSerializer


class CustomTokenCreateView(ObtainAuthToken):
    """Custom ObtainAuthToken that checks if user is verified."""

    permission_classes = (AllowAny,)
    my_tags = ['token-auth']

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if not user.is_verified:
            raise AuthenticationFailed('User is not verified.')
        token, created = Token.objects.get_or_create(user=user)
        return Response({'auth_token': token.key})


class TokenDestroyView(APIView):
    """Custom TokenDestroyView that deletes the auth-token."""

    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            return Response(
                {'detail': 'User was not logged in.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom TokenObtainPairView that uses CustomTokenObtainPairSerializer to check if TicketHolder.is_verified ==
    True."""

    serializer_class = CustomTokenObtainPairSerializer

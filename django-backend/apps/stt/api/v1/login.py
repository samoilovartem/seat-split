from djoser.views import TokenCreateView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.stt.api.v1.serializers import CustomTokenObtainPairSerializer


class CustomTokenCreateView(TokenCreateView):
    """Custom TokenCreateView that checks if user is verified."""

    permission_classes = (AllowAny,)

    def _action(self, serializer):
        user = serializer.user
        if not user.is_verified:
            raise AuthenticationFailed('User is not verified.')
        return super()._action(serializer)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom TokenObtainPairView that uses CustomTokenObtainPairSerializer to check if TicketHolder.is_verified ==
    True."""

    serializer_class = CustomTokenObtainPairSerializer

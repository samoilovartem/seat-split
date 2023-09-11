from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


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

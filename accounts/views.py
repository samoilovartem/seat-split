from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey

from .models import Accounts
from .pagination import AccountsApiListPagination
from .serializers import AccountsSerializer


class AllAccountsViewSet(viewsets.ModelViewSet):
    queryset = Accounts.objects.all()
    serializer_class = AccountsSerializer
    pagination_class = AccountsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]
    filterset_fields = '__all__'
    my_tags = ["All accounts"]

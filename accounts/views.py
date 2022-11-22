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
    my_tags = ["All accounts"]


class AccountsUniversalFilterViewSet(viewsets.ModelViewSet):
    serializer_class = AccountsSerializer
    pagination_class = AccountsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]
    my_tags = ["Accounts universal filter"]

    def get_queryset(self):
        filter_name = self.request.query_params.get('filter_name')
        value = self.request.query_params.get('value')
        return Accounts.objects.filter(**{f"{filter_name}__icontains": value})

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import IsAuthenticated
from .serializers import AccountsSerializer
from .pagination import AccountsApiListPagination

from .models import Accounts


class LawnsAccountsViewSet(viewsets.ModelViewSet):
    serializer_class = AccountsSerializer
    pagination_class = AccountsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]

    """
    get_queryset() allows us to redefine existing queryset method.
    We can use it in case we want to filter or sort our fata.
    """

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Accounts.objects.filter(team__icontains='LAWNS')
        return Accounts.objects.filter(team__icontains='LAWNS', pk=pk)

    """
    @action allows us to set custom routes.
    The function's name is url route itself. For example:
    api/v1/accounts/presales_accounts/
    """

    # @action(methods=['get'], detail=False)
    # def presales_accounts(self, request):
    #     presales_accounts = Accounts.objects.filter(team__icontains='presales').values()
    #     return Response({'results': presales_accounts})


class PresalesAccountsViewSet(viewsets.ModelViewSet):
    serializer_class = AccountsSerializer
    pagination_class = AccountsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Accounts.objects.filter(team__icontains='PRESALES')
        return Accounts.objects.filter(team__icontains='PRESALES', pk=pk)


class MLBAccountsViewSet(viewsets.ModelViewSet):
    serializer_class = AccountsSerializer
    pagination_class = AccountsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Accounts.objects.filter(team__icontains='MLB')
        return Accounts.objects.filter(team__icontains='MLB', pk=pk)


class NBAAccountsViewSet(viewsets.ModelViewSet):
    serializer_class = AccountsSerializer
    pagination_class = AccountsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Accounts.objects.filter(team__icontains='NBA')
        return Accounts.objects.filter(team__icontains='NBA', pk=pk)


class SeasonsAccountsViewSet(viewsets.ModelViewSet):
    serializer_class = AccountsSerializer
    pagination_class = AccountsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Accounts.objects.filter(team__icontains='SEASONS')
        return Accounts.objects.filter(team__icontains='SEASONS', pk=pk)


class SmallVenuesAccountsViewSet(viewsets.ModelViewSet):
    serializer_class = AccountsSerializer
    pagination_class = AccountsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Accounts.objects.filter(team__icontains='SMALL VENUES')
        return Accounts.objects.filter(team__icontains='SMALL VENUES', pk=pk)


class TheatreAccountsViewSet(viewsets.ModelViewSet):
    serializer_class = AccountsSerializer
    pagination_class = AccountsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Accounts.objects.filter(team__icontains='THEATRE')
        return Accounts.objects.filter(team__icontains='THEATRE', pk=pk)


class OtherSportsAccountsViewSet(viewsets.ModelViewSet):
    serializer_class = AccountsSerializer
    pagination_class = AccountsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Accounts.objects.filter(team__icontains='OTHER SPORTS')
        return Accounts.objects.filter(team__icontains='OTHER SPORTS', pk=pk)


class AudreyAccountsViewSet(viewsets.ModelViewSet):
    serializer_class = AccountsSerializer
    pagination_class = AccountsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Accounts.objects.filter(team__icontains='AUDREY')
        return Accounts.objects.filter(team__icontains='AUDREY', pk=pk)




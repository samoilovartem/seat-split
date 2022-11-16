from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import IsAuthenticated
from .serializers import AccountsSerializer
from .pagination import AccountsApiListPagination

from .models import Accounts


class AllAccountsViewSet(viewsets.ModelViewSet):
    queryset = Accounts.objects.all()
    serializer_class = AccountsSerializer
    pagination_class = AccountsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]
    my_tags = ["All accounts"]


class LawnsAccountsViewSet(viewsets.ModelViewSet):
    serializer_class = AccountsSerializer
    pagination_class = AccountsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]
    my_tags = ["Lawns accounts"]

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Accounts.objects.filter(team__icontains='LAWNS')
        return Accounts.objects.filter(team__icontains='LAWNS', pk=pk)

    @action(methods=['get'], detail=False)
    def get_creators(self, request):
        result = Accounts.objects.filter(team__icontains='LAWNS') \
            .order_by().values_list('created_by', flat=True).distinct()
        return Response({'results': {'All creators': result}})


class PresalesAccountsViewSet(viewsets.ModelViewSet):
    serializer_class = AccountsSerializer
    pagination_class = AccountsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]
    my_tags = ["Presales accounts"]

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Accounts.objects.filter(team__icontains='PRESALES')
        return Accounts.objects.filter(team__icontains='PRESALES', pk=pk)


class MLBAccountsViewSet(viewsets.ModelViewSet):
    serializer_class = AccountsSerializer
    pagination_class = AccountsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]
    my_tags = ["MLB accounts"]

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Accounts.objects.filter(team__icontains='MLB')
        return Accounts.objects.filter(team__icontains='MLB', pk=pk)


class NBAAccountsViewSet(viewsets.ModelViewSet):
    serializer_class = AccountsSerializer
    pagination_class = AccountsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]
    my_tags = ["NBA accounts"]

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Accounts.objects.filter(team__icontains='NBA')
        return Accounts.objects.filter(team__icontains='NBA', pk=pk)


class SeasonsAccountsViewSet(viewsets.ModelViewSet):
    serializer_class = AccountsSerializer
    pagination_class = AccountsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]
    my_tags = ["Seasons accounts"]

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Accounts.objects.filter(team__icontains='SEASONS')
        return Accounts.objects.filter(team__icontains='SEASONS', pk=pk)


class SmallVenuesAccountsViewSet(viewsets.ModelViewSet):
    serializer_class = AccountsSerializer
    pagination_class = AccountsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]
    my_tags = ["Small Venues accounts"]

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Accounts.objects.filter(team__icontains='SMALL VENUES')
        return Accounts.objects.filter(team__icontains='SMALL VENUES', pk=pk)


class TheatreAccountsViewSet(viewsets.ModelViewSet):
    serializer_class = AccountsSerializer
    pagination_class = AccountsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]
    my_tags = ["Theatre accounts"]

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Accounts.objects.filter(team__icontains='THEATRE')
        return Accounts.objects.filter(team__icontains='THEATRE', pk=pk)


class OtherSportsAccountsViewSet(viewsets.ModelViewSet):
    serializer_class = AccountsSerializer
    pagination_class = AccountsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]
    my_tags = ["Other Sports accounts"]

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Accounts.objects.filter(team__icontains='OTHER SPORTS')
        return Accounts.objects.filter(team__icontains='OTHER SPORTS', pk=pk)


class AudreyAccountsViewSet(viewsets.ModelViewSet):
    serializer_class = AccountsSerializer
    pagination_class = AccountsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]
    my_tags = ["Audrey accounts"]

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Accounts.objects.filter(team__icontains='AUDREY')
        return Accounts.objects.filter(team__icontains='AUDREY', pk=pk)


class OthersAccountsViewSet(viewsets.ModelViewSet):
    serializer_class = AccountsSerializer
    pagination_class = AccountsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]
    my_tags = ["Others accounts"]

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Accounts.objects.filter(team__icontains='OTHERS')
        return Accounts.objects.filter(team__icontains='OTHERS', pk=pk)




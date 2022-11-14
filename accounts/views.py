from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import IsAuthenticated
from .serializers import AccountsSerializer
from .pagination import AccountsApiListPagination

from .models import Accounts


# class AccountsApiList(ListCreateAPIView):
#     queryset = Accounts.objects.all()
#     serializer_class = AccountsSerializer
#     pagination_class = AccountsApiListPagination
#     # permission_classes = [HasAPIKey | IsAuthenticated]
#     permission_classes = [IsAuthenticated]
#
#
# class AccountsApiRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
#     queryset = Accounts.objects.all()
#     serializer_class = AccountsSerializer
#     # permission_classes = [HasAPIKey | IsAuthenticated]
#     permission_classes = [IsAuthenticated]


class AccountsViewSet(viewsets.ModelViewSet):
    queryset = Accounts.objects.all()
    serializer_class = AccountsSerializer
    pagination_class = AccountsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]

    """
    get_queryset() allows us to redefine existing queryset method.
    We can use it in case we want to filter or sort our fata.
    """

    # def get_queryset(self):
    #     pk = self.kwargs.get('pk')
    #
    #     if not pk:
    #         return Accounts.objects.all()[:3]
    #     return Accounts.objects.filter(pk=pk)

    """
    @action allows us to set custom routes.
    The function's name is url route itself. For example:
    api/v1/accounts/presales_accounts/
    """

    @action(methods=['get'], detail=False)
    def presales_accounts(self, request):
        presales_accounts = Accounts.objects.filter(team__icontains='presales').values()
        return Response({'results': presales_accounts})

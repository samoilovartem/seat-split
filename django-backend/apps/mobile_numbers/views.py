from rest_flex_fields import FlexFieldsModelViewSet, is_expanded
from rest_framework.decorators import action
from rest_framework.response import Response

from django.db.models import Prefetch

from apps.accounts.models import Accounts
from apps.mobile_numbers.filters import MobileNumbersFilterSet
from apps.mobile_numbers.models import MobileNumberTransaction
from apps.mobile_numbers.serializers import MobileNumbersSerializer
from apps.users.models import User
from apps.utils.utils import records_per_value


class AllMobileNumbersViewSet(FlexFieldsModelViewSet):
    def get_queryset(self):
        queryset = MobileNumberTransaction.objects.all()
        if is_expanded(self.request, '*'):
            queryset = queryset.prefetch_related(
                Prefetch('email', queryset=Accounts.objects.only('id', 'email')),
                Prefetch('requested_by', queryset=User.objects.only('id', 'username')),
            )
        elif is_expanded(self.request, 'email'):
            queryset = queryset.prefetch_related(
                Prefetch('email', queryset=Accounts.objects.only('id', 'email'))
            )
        elif is_expanded(self.request, 'requested_by'):
            queryset = queryset.prefetch_related(
                Prefetch('requested_by', queryset=User.objects.only('id', 'username'))
            )
        return queryset

    permit_list_expands = ['email', 'requested_by']
    serializer_class = MobileNumbersSerializer
    filterset_class = MobileNumbersFilterSet

    search_fields = (
        'email',
        'phone',
    )
    ordering_fields = (
        'id',
        'created_at',
    )
    my_tags = ['All mobile number transactions']

    @action(methods=['GET'], detail=False)
    def get_mobile_numbers_per_service(self, request):
        result = records_per_value(MobileNumberTransaction, 'service_name')
        return Response({'results': result})

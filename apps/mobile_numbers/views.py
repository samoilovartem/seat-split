from rest_flex_fields import FlexFieldsModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.mobile_numbers.filters import MobileNumbersFilterSet
from apps.mobile_numbers.models import MobileNumberTransaction
from apps.mobile_numbers.serializers import MobileNumbersSerializer
from apps.mobile_numbers.utils import mobile_numbers_per_value


class AllMobileNumbersViewSet(FlexFieldsModelViewSet):
    queryset = MobileNumberTransaction.objects.all().select_related(
        'email', 'requested_by'
    )
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
        result = mobile_numbers_per_value('service_name')
        return Response({'results': result})

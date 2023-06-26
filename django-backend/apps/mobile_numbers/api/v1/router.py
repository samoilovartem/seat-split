from rest_framework import routers

from apps.mobile_numbers.api.v1.mobile_numbers import AllMobileNumbersViewSet

mobile_numbers_router_v1 = routers.SimpleRouter()
mobile_numbers_router_v1.register(
    r'mobile-number-transactions',
    AllMobileNumbersViewSet,
    basename='all-mobile-numbers',
)

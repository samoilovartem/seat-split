from rest_framework import routers

from apps.mobile_numbers.views import AllMobileNumbersViewSet

mobile_numbers_router = routers.SimpleRouter()
mobile_numbers_router.register(
    r'mobile-number-transactions',
    AllMobileNumbersViewSet,
    basename='all-mobile-numbers',
)

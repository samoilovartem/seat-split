from apps.mobile_numbers.views import AllMobileNumbersViewSet
from rest_framework import routers

mobile_numbers_router = routers.SimpleRouter()
mobile_numbers_router.register(
    r'mobile-number-transactions',
    AllMobileNumbersViewSet,
    basename='all-mobile-numbers',
)

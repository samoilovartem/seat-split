from rest_framework.routers import SimpleRouter

from apps.us_addresses.views import AddressesWithinDistanceViewSet

us_address_router = SimpleRouter()
us_address_router.register(
    r'addresses_within_distance',
    AddressesWithinDistanceViewSet,
    basename='addresses_within_distance',
)

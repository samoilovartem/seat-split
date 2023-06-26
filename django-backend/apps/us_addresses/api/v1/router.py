from rest_framework.routers import SimpleRouter

from apps.us_addresses.api.v1.us_addresses import AddressesWithinDistanceViewSet

us_address_router_v1 = SimpleRouter()
us_address_router_v1.register(
    r'addresses_within_distance',
    AddressesWithinDistanceViewSet,
    basename='addresses-within-distance',
)

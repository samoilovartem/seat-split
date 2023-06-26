from rest_framework import routers

from apps.us_addresses.api.v1.router import us_address_router_v1

us_addresses_api_router_v1 = routers.DefaultRouter()
us_addresses_api_router_v1.registry.extend(us_address_router_v1.registry)

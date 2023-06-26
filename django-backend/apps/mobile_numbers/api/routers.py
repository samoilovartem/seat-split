from rest_framework import routers

from apps.mobile_numbers.api.v1.router import mobile_numbers_router_v1

mobile_numbers_api_router_v1 = routers.DefaultRouter()
mobile_numbers_api_router_v1.registry.extend(mobile_numbers_router_v1.registry)

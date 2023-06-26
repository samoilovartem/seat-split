from rest_framework import routers

from apps.venues.api.v1.router import venues_router

venues_api_router_v1 = routers.DefaultRouter()
venues_api_router_v1.registry.extend(venues_router.registry)

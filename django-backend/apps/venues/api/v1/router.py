from rest_framework import routers

from apps.venues.api.v1.venues import AllVenuesViewSet

venues_router = routers.SimpleRouter()
venues_router.register(r'venues', AllVenuesViewSet, basename='all-venues')

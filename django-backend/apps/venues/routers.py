from rest_framework import routers

from apps.venues.views import AllVenuesViewSet

venues_router = routers.SimpleRouter()
venues_router.register(r'venues', AllVenuesViewSet, basename='all-venues')

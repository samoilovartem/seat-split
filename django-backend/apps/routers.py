from rest_framework import routers

from apps.stt.api import stt_api_router_v1

main_router = routers.DefaultRouter()
main_router.registry.extend(stt_api_router_v1.registry)

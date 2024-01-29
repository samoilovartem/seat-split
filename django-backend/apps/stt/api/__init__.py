from apps.stt.api.v1 import stt_router_v1
from rest_framework import routers

stt_api_router_v1 = routers.DefaultRouter()
stt_api_router_v1.registry.extend(stt_router_v1.registry)

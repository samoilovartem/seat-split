from rest_framework import routers

from apps.in_app_notifications.api import in_app_notifications_api_router_v1
from apps.stt.api.routers import stt_api_router_v1
from apps.users.api import users_api_router_v1

main_router = routers.DefaultRouter()
main_router.registry.extend(stt_api_router_v1.registry)
main_router.registry.extend(users_api_router_v1.registry)
main_router.registry.extend(in_app_notifications_api_router_v1.registry)

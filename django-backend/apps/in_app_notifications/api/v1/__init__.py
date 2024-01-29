from apps.in_app_notifications.api.v1.notifications import NotificationViewSet
from rest_framework import routers

in_app_notifications_router_v1 = routers.DefaultRouter()
in_app_notifications_router_v1.register(r'notifications', NotificationViewSet, basename='notifications')

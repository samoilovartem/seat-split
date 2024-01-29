from apps.users.api.v1 import users_router_v1
from rest_framework import routers

users_api_router_v1 = routers.DefaultRouter()
users_api_router_v1.registry.extend(users_router_v1.registry)

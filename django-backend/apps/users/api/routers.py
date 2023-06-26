from rest_framework import routers

from apps.users.api.v1.routers import groups_router_v1, users_router_v1

users_groups_router_v1 = routers.DefaultRouter()
users_groups_router_v1.registry.extend(users_router_v1.registry)
users_groups_router_v1.registry.extend(groups_router_v1.registry)

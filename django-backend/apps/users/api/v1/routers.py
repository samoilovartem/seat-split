from rest_framework import routers

from apps.users.api.v1.groups import GroupViewSet
from apps.users.api.v1.users import UsersViewSet

users_router_v1 = routers.SimpleRouter()
groups_router_v1 = routers.SimpleRouter()

users_router_v1.register(r'users', UsersViewSet, basename='all-users')
groups_router_v1.register(r'groups', GroupViewSet, basename='all-groups')

from rest_framework import routers

from apps.users.api.v1.users import UserViewSet

users_router_v1 = routers.DefaultRouter()
users_router_v1.register(r'auth/users', UserViewSet, basename='users')

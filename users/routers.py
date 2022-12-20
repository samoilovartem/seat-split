from rest_framework import routers
from .views import *

users_router = routers.SimpleRouter()
groups_router = routers.SimpleRouter()

users_router.register(r'users', UsersViewSet, basename='all-users')
groups_router.register(r'groups', GroupViewSet, basename='all-groups')

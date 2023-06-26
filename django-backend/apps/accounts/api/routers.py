from rest_framework import routers

from apps.accounts.api.v1.router import accounts_router_v1

accounts_api_router_v1 = routers.DefaultRouter()
accounts_api_router_v1.registry.extend(accounts_router_v1.registry)

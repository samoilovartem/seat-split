from rest_framework import routers

from apps.accounts.api.v1.accounts import AllAccountsViewSet

accounts_router_v1 = routers.DefaultRouter()
accounts_router_v1.register(r'accounts', AllAccountsViewSet, basename='all-accounts')

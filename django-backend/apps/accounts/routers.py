from rest_framework import routers

from apps.accounts.views import AllAccountsViewSet

accounts_router = routers.SimpleRouter()
accounts_router.register(r'accounts', AllAccountsViewSet, basename='all-accounts')

from apps.accounts.views import AllAccountsViewSet
from rest_framework import routers

accounts_router = routers.SimpleRouter()
accounts_router.register(r'accounts', AllAccountsViewSet, basename='all-accounts')

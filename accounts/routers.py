from rest_framework import routers
from .views import *

accounts_router = routers.SimpleRouter()


accounts_router.register(r'accounts/all', AllAccountsViewSet, basename='all-accounts')
accounts_router.register(r'accounts/universal_filter', AccountsUniversalFilterViewSet,
                         basename='accounts_universal_filter')

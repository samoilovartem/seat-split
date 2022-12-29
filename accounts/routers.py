from rest_framework import routers
from accounts.views import *

accounts_router = routers.SimpleRouter()
accounts_router.register(r'accounts', AllAccountsViewSet, basename='all-accounts')

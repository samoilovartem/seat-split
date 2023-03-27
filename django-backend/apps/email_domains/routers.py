from apps.email_domains.views import AllEmailDomainsViewSet
from rest_framework import routers

email_domains_router = routers.SimpleRouter()
email_domains_router.register(
    r'email-domains',
    AllEmailDomainsViewSet,
    basename='all-email-domains',
)

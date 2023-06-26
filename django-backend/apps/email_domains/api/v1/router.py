from rest_framework import routers

from apps.email_domains.api.v1.email_domains import AllEmailDomainsViewSet

email_domains_router_v1 = routers.SimpleRouter()
email_domains_router_v1.register(
    r'email-domains',
    AllEmailDomainsViewSet,
    basename='all-email-domains',
)

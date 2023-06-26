from rest_framework import routers

from apps.email_domains.api.v1.router import email_domains_router_v1

email_domains_api_router_v1 = routers.DefaultRouter()
email_domains_api_router_v1.registry.extend(email_domains_router_v1.registry)

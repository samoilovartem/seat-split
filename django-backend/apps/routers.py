from rest_framework import routers

from apps.accounts.api.routers import accounts_api_router_v1
from apps.cards.api.routers import cards_api_router_v1
from apps.email_domains.api.routers import email_domains_api_router_v1
from apps.mobile_numbers.api.routers import mobile_numbers_api_router_v1
from apps.us_addresses.api.routers import us_addresses_api_router_v1
from apps.users.api.routers import users_groups_router_v1
from apps.venues.api.routers import venues_api_router_v1

main_router = routers.DefaultRouter()

main_router.registry.extend(accounts_api_router_v1.registry)
main_router.registry.extend(cards_api_router_v1.registry)
main_router.registry.extend(email_domains_api_router_v1.registry)
main_router.registry.extend(mobile_numbers_api_router_v1.registry)
main_router.registry.extend(us_addresses_api_router_v1.registry)
main_router.registry.extend(users_groups_router_v1.registry)
main_router.registry.extend(venues_api_router_v1.registry)

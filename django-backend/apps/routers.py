from rest_framework import routers

from apps.accounts.routers import accounts_router
from apps.cards.routers import cards_router
from apps.email_domains.routers import email_domains_router
from apps.mobile_numbers.routers import mobile_numbers_router
from apps.us_addresses.routers import us_address_router
from apps.users.routers import groups_router, users_router
from apps.venues.routers import venues_router

main_router = routers.DefaultRouter()

main_router.registry.extend(cards_router.registry)
main_router.registry.extend(accounts_router.registry)
main_router.registry.extend(users_router.registry)
main_router.registry.extend(groups_router.registry)
main_router.registry.extend(mobile_numbers_router.registry)
main_router.registry.extend(email_domains_router.registry)
main_router.registry.extend(us_address_router.registry)
main_router.registry.extend(venues_router.registry)

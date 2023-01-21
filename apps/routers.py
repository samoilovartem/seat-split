from rest_framework import routers

from apps.accounts.routers import accounts_router
from apps.cards.routers import cards_router
from apps.users.routers import groups_router, users_router

main_router = routers.DefaultRouter()

main_router.registry.extend(cards_router.registry)
main_router.registry.extend(accounts_router.registry)
main_router.registry.extend(users_router.registry)
main_router.registry.extend(groups_router.registry)

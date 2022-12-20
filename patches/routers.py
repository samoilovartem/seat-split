from rest_framework import routers
from accounts.routers import accounts_router
from cards.routers import cards_router
from users.routers import users_router, groups_router

main_router = routers.DefaultRouter()

main_router.registry.extend(cards_router.registry)
main_router.registry.extend(accounts_router.registry)
main_router.registry.extend(users_router.registry)
main_router.registry.extend(groups_router.registry)

from rest_framework import routers
from accounts.routers import accounts_router
from cards.routers import cards_router
from sold_inventory.routers import sold_inventory_router

main_router = routers.DefaultRouter()

main_router.registry.extend(cards_router.registry)
main_router.registry.extend(accounts_router.registry)
main_router.registry.extend(sold_inventory_router.registry)

from rest_framework import routers

from apps.cards.api.v1.router import cards_router_v1

cards_api_router_v1 = routers.DefaultRouter()
cards_api_router_v1.registry.extend(cards_router_v1.registry)

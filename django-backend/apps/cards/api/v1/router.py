from rest_framework import routers

from apps.cards.api.v1.cards import AllCardsViewSet

cards_router_v1 = routers.SimpleRouter()

cards_router_v1.register(r'cards', AllCardsViewSet, basename='all-cards')

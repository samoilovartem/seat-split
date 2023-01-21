from rest_framework import routers

from apps.cards.views import AllCardsViewSet

cards_router = routers.SimpleRouter()

cards_router.register(r'cards', AllCardsViewSet, basename='all-cards')

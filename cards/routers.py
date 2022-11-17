from rest_framework import routers

from .views import *

all_cards_router = routers.DefaultRouter()
lawns_router = routers.DefaultRouter()
presales_router = routers.DefaultRouter()
mlb_router = routers.DefaultRouter()
nba_router = routers.DefaultRouter()
seasons_router = routers.DefaultRouter()
small_venues_router = routers.DefaultRouter()
theatre_router = routers.DefaultRouter()
other_sports_router = routers.DefaultRouter()
audrey_router = routers.DefaultRouter()
others_router = routers.DefaultRouter()


all_cards_router.register(r'cards/all', AllCardsViewSet, basename='all-cards')
lawns_router.register(r'cards/lawns', LawnsCardsViewSet, basename='lawns-cards')
presales_router.register(r'cards/presales', PresalesCardsViewSet, basename='presales-cards')
mlb_router.register(r'cards/mlb', MLBCardsViewSet, basename='mlb-cards')
nba_router.register(r'cards/nba', NBACardsViewSet, basename='nba-cards')
seasons_router.register(r'cards/seasons', SeasonsCardsViewSet, basename='seasons-cards')
small_venues_router.register(r'cards/smallvenues', SmallVenuesCardsViewSet, basename='smallvenues-cards')
theatre_router.register(r'cards/theatre', TheatreCardsViewSet, basename='theatre-cards')
other_sports_router.register(r'cards/othersports', OtherSportsCardsViewSet, basename='othersports-cards')
audrey_router.register(r'cards/audrey', AudreyCardsViewSet, basename='audrey-cards')
others_router.register(r'cards/others', OthersCardsViewSet, basename='others-cards')


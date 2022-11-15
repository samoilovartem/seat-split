from rest_framework import routers

from .views import *

all_accounts_router = routers.DefaultRouter()
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


all_accounts_router.register(r'accounts/all', AllAccountsViewSet, basename='all-accounts')
lawns_router.register(r'accounts/lawns', LawnsAccountsViewSet, basename='lawns-accounts')
presales_router.register(r'accounts/presales', PresalesAccountsViewSet, basename='presales-accounts')
mlb_router.register(r'accounts/mlb', MLBAccountsViewSet, basename='mlb-accounts')
nba_router.register(r'accounts/nba', NBAAccountsViewSet, basename='nba-accounts')
seasons_router.register(r'accounts/seasons', SeasonsAccountsViewSet, basename='seasons-accounts')
small_venues_router.register(r'accounts/smallvenues', SmallVenuesAccountsViewSet, basename='smallvenues-accounts')
theatre_router.register(r'accounts/theatre', TheatreAccountsViewSet, basename='theatre-accounts')
other_sports_router.register(r'accounts/othersports', OtherSportsAccountsViewSet, basename='othersports-accounts')
audrey_router.register(r'accounts/audrey', AudreyAccountsViewSet, basename='audrey-accounts')
others_router.register(r'accounts/others', OthersAccountsViewSet, basename='others-accounts')


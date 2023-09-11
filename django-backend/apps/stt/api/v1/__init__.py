from rest_framework import routers

from apps.stt.api.v1.teams import TeamViewSet
from apps.stt.api.v1.ticket_holders import TicketHolderViewSet

stt_router_v1 = routers.DefaultRouter()
stt_router_v1.register(r'teams', TeamViewSet, basename='all-teams')
stt_router_v1.register(
    r'ticket-holders', TicketHolderViewSet, basename='all-ticket-holders'
)

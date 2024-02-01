from django.db import models

from apps.stt.models.event import Event  # noqa
from apps.stt.models.purchase import Purchase  # noqa
from apps.stt.models.season import Season  # noqa
from apps.stt.models.team import Team  # noqa
from apps.stt.models.team_event import TeamEvent  # noqa
from apps.stt.models.ticket import Ticket  # noqa
from apps.stt.models.ticket_holder import (
    ticket_holder_avatar_path as new_ticket_holder_avatar_path,
)
from apps.stt.models.ticket_holder_team import TicketHolderTeam  # noqa
from apps.stt.models.venue import Venue  # noqa

teams_events = models.ManyToManyField(Team, through='TeamEvent')
ticket_holders_teams = models.ManyToManyField(Team, through='TicketHolderTeam')


def ticket_holder_avatar_path(*args, **kwargs):
    return new_ticket_holder_avatar_path(*args, **kwargs)

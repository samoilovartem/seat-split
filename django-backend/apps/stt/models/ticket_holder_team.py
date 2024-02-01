from uuid import uuid4

from django_cryptography.fields import encrypt
from simple_history.models import HistoricalRecords

from django.db import models
from django.db.models import UniqueConstraint

from apps.stt.models.team import Team
from apps.stt.models.ticket_holder import TicketHolder


class TicketHolderTeam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    ticket_holder = models.ForeignKey(
        TicketHolder, related_name='ticket_holder_teams', on_delete=models.CASCADE
    )
    team = models.ForeignKey(Team, related_name='ticket_holder_teams', on_delete=models.CASCADE)
    section = models.CharField(max_length=255)
    row = models.CharField(max_length=255)
    seat = models.CharField(max_length=255)
    seats_quantity = models.PositiveIntegerField(default=1, editable=False)
    credentials_website_username = encrypt(models.CharField(max_length=255))
    credentials_website_password = encrypt(models.CharField(max_length=255))
    is_confirmed = models.BooleanField(default=False, help_text="Is the ticket holder's team data confirmed?")
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        db_table = 'content"."ticket_holder_team'
        verbose_name = "Ticket Holder's Team"
        verbose_name_plural = "Ticket Holder's Teams"
        permissions = (('view_credentials', 'Can view credentials'),)
        constraints = (
            UniqueConstraint(
                fields=('ticket_holder', 'team'),
                name='ticket_holder_team_idx',
            ),
        )

    def save(self, *args, **kwargs):
        self.seats_quantity = self.calculate_quantity()
        super(TicketHolderTeam, self).save(*args, **kwargs)

    def calculate_quantity(self):
        if '-' in self.seat:
            first_seat, last_seat = map(int, self.seat.split('-'))
            return last_seat - first_seat + 1
        return 1

    def __str__(self):
        return f'{self.ticket_holder} - {self.team} - {self.team.id}'

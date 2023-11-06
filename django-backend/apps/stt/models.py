from uuid import uuid4

from simple_history.models import HistoricalRecords

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class TicketHolder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    user = models.OneToOneField(
        User, related_name='ticket_holder_user', on_delete=models.CASCADE
    )
    phone = models.CharField(
        verbose_name='Phone number',
        blank=True,
        max_length=255,
    )
    address = models.CharField(max_length=255, blank=True)
    is_card_interest = models.BooleanField(default=False)
    is_season_ticket_interest = models.BooleanField(default=False)
    tickets_data = models.JSONField(null=True, blank=True, default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        db_table = "content\".\"ticket_holder"
        verbose_name = 'Ticket Holder'
        verbose_name_plural = 'Ticket Holders'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    ticket_holder = models.ForeignKey(TicketHolder, on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='tickets')
    season = models.CharField(max_length=255)
    skybox_event_id = models.CharField(max_length=255, blank=True, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seat = models.CharField(max_length=255)
    row = models.CharField(max_length=255)
    section = models.CharField(max_length=255)
    barcode = models.CharField(max_length=255, blank=True, default='')
    listing_status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    sold_at = models.DateTimeField(null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table = "content\".\"ticket"
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
        constraints = (
            UniqueConstraint(
                fields=('ticket_holder', 'event', 'seat'),
                name='unique_ticket',
            ),
        )

    def __str__(self):
        return f'{self.ticket_holder} - {self.event} - {self.id}'


class Purchase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=255, blank=True, default='')
    customer = models.CharField(max_length=255)
    purchased_at = models.DateTimeField(null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        db_table = "content\".\"purchase"
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'

    def __str__(self):
        return f'{self.ticket} - {self.invoice_number}'


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    season = models.CharField(max_length=255)
    history = HistoricalRecords()

    class Meta:
        db_table = "content\".\"event"
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        constraints = (
            UniqueConstraint(
                fields=('name', 'date_time', 'season'),
                name='name_date_time_season_idx',
            ),
        )
        permissions = (
            ('import_events', 'Can import'),
            ('export_events', 'Can export'),
        )

    def __str__(self):
        return f'{self.name} | {self.date_time.strftime("%m/%d/%Y, %H:%M:%S")}'


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    name_short = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=255)
    league = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    home_venue = models.CharField(max_length=255)
    ticketmaster_id = models.IntegerField()
    timezone = models.CharField(max_length=255)
    credentials_website = models.CharField(max_length=255)
    ticketmaster_name = models.CharField(max_length=255)

    class Meta:
        db_table = "content\".\"team"
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
        permissions = (
            ('import_events', 'Can import'),
            ('export_events', 'Can export'),
        )

    def __str__(self):
        return f'{self.name}'


teams_events = models.ManyToManyField(Team, through='TeamEvent')


class TeamEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "content\".\"team_event"
        verbose_name = "Event's Team"
        verbose_name_plural = "Event's Teams"
        constraints = (
            UniqueConstraint(
                fields=('event', 'team'),
                name='event_team_idx',
            ),
        )

    def __str__(self):
        return f'{self.event} - {self.team} - {self.id}'


class TicketHolderTeam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    ticket_holder = models.ForeignKey(
        TicketHolder, related_name='ticket_holder_teams', on_delete=models.CASCADE
    )
    team = models.ForeignKey(
        Team, related_name='ticket_holder_teams', on_delete=models.CASCADE
    )
    section = models.CharField(max_length=255)
    row = models.CharField(max_length=255)
    seat = models.CharField(max_length=255)
    seats_quantity = models.PositiveIntegerField(default=1, editable=False)
    credentials_website_username = models.CharField(max_length=255)
    credentials_website_password = models.CharField(max_length=255)
    is_confirmed = models.BooleanField(
        default=False, help_text="Is the ticket holder's team data confirmed?"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "content\".\"ticket_holder_team"
        verbose_name = "Ticket Holder's Team"
        verbose_name_plural = "Ticket Holder's Teams"
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
        # Use the same logic as in validate_seat_range for calculating quantity.
        if '-' in self.seat:
            first_seat, last_seat = map(int, self.seat.split('-'))
            return last_seat - first_seat + 1
        return 1

    def __str__(self):
        return f'{self.ticket_holder} - {self.team} - {self.team.id}'


ticket_holders_teams = models.ManyToManyField(Team, through='TicketHolderTeam')

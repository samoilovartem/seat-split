from hashlib import md5
from uuid import uuid4

from django_cryptography.fields import encrypt
from pytz import all_timezones
from simple_history.models import HistoricalRecords

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.timezone import now

from config.components.business_related import SUPPORTED_LEAGUES

User = get_user_model()


def ticket_holder_avatar_path(instance, filename):
    """Generate unique path for ticket holder avatar."""
    ext = filename.split('.')[-1]

    unique_filename = f'{uuid4().hex}.{ext}'

    user = instance.user
    hash_string = md5(f'{user.email}{user.id}'.encode()).hexdigest()

    return f'avatars/{hash_string}/{unique_filename}'


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
    created_at = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(
        upload_to=ticket_holder_avatar_path, null=True, blank=True
    )
    timezone = models.CharField(
        max_length=255, choices=[(tz, tz) for tz in all_timezones], default='UTC'
    )
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

    def save(self, *args, **kwargs):
        if self.listing_status == 'Sold' and not self.sold_at:
            self.sold_at = now()
        super(Ticket, self).save(*args, **kwargs)

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
    skybox_event_id = models.CharField(max_length=255, blank=True, default='')
    name = models.CharField(max_length=255)
    additional_info = models.CharField(max_length=255, default='')
    date_time = models.DateTimeField()
    season = models.CharField(max_length=255)
    venue = models.ForeignKey(
        'Venue', on_delete=models.SET_NULL, null=True, related_name='events'
    )
    stubhub_event_url = models.TextField(blank=True, default='')
    league = models.CharField(max_length=255)
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
        return f'{self.name} | {self.date_time.strftime("%m/%d/%Y")}'


class Venue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    skybox_venue_id = models.IntegerField()
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    timezone = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

    class Meta:
        db_table = "content\".\"venue"
        verbose_name = 'Venue'
        verbose_name_plural = 'Venues'
        permissions = (
            ('import_events', 'Can import'),
            ('export_events', 'Can export'),
        )
        constraints = (
            UniqueConstraint(
                fields=('skybox_venue_id', 'name'),
                name='skybox_venue_id_name_idx',
            ),
        )

    def __str__(self):
        return f'{self.name}'


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    skybox_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255)
    name_short = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=255)
    league = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    home_venue = models.ForeignKey(
        Venue, on_delete=models.PROTECT, null=True, related_name='home_teams'
    )
    logo = models.FileField(upload_to='logos/', null=True, blank=True)
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


class Season(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(
        max_length=255,
        help_text='The name or title of the season. For example, "2023", "2023-2024".',
    )
    start_year = models.IntegerField(
        help_text='The calendar year when the season starts'
    )
    league = models.CharField(
        max_length=255,
        choices=((league, league) for league in SUPPORTED_LEAGUES),
        help_text='The sports league to which the season belongs',
    )
    official_start_date = models.DateField(
        blank=True, help_text='The date when the season officially starts'
    )
    official_end_date = models.DateField(
        blank=True, help_text='The date when the season officially ends'
    )

    start_selling_season_date = models.DateField(
        blank=True, help_text='The date when sales for season-related tickets begin'
    )

    start_regular_season_date = models.DateField(
        blank=True, help_text='The date when the regular season is scheduled to begin'
    )
    end_regular_season_date = models.DateField(
        blank=True, help_text='The date when the regular season is scheduled to end'
    )

    start_playoff_date = models.DateField(
        blank=True, help_text='The date when the playoff season is scheduled to begin'
    )
    end_playoff_date = models.DateField(
        blank=True, help_text='The date when the playoff season is scheduled to end'
    )

    is_selling_season = models.BooleanField(
        default=False,
        help_text='A boolean indicating if the season is currently in the selling period',
    )
    is_regular_season = models.BooleanField(
        default=False,
        help_text='A boolean indicating if the season is currently in the regular season period',
    )
    is_playoff_season = models.BooleanField(
        default=False,
        help_text='A boolean indicating if the season is currently in the playoff period',
    )
    history = HistoricalRecords()

    class Meta:
        db_table = "content\".\"season"
        verbose_name = 'Season'
        verbose_name_plural = 'Seasons'
        constraints = (
            UniqueConstraint(
                fields=('name', 'league', 'start_year'),
                name='unique_season_details',
            ),
        )

    def __str__(self):
        return f'{self.name}'


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
    credentials_website_username = encrypt(models.CharField(max_length=255))
    credentials_website_password = encrypt(models.CharField(max_length=255))
    is_confirmed = models.BooleanField(
        default=False, help_text="Is the ticket holder's team data confirmed?"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "content\".\"ticket_holder_team"
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


ticket_holders_teams = models.ManyToManyField(Team, through='TicketHolderTeam')

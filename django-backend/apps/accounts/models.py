from simple_history.models import HistoricalRecords

from django.contrib.auth import get_user_model
from django.db import models

from apps.validators import any_or_na

User = get_user_model()


class Accounts(models.Model):
    """Table that contains all company's accounts"""

    first_name = models.CharField(max_length=100, validators=[any_or_na])
    last_name = models.CharField(max_length=100, validators=[any_or_na])
    email = models.EmailField(max_length=150)
    type = models.CharField(max_length=100, validators=[any_or_na])
    password = models.CharField(max_length=32, validators=[any_or_na])
    delta_created = models.BooleanField(default=False)
    delta_password = models.CharField(
        max_length=32, validators=[any_or_na], default='NA'
    )
    delta_miles = models.CharField(max_length=100, default='NA')
    flyingblue_miles = models.CharField(max_length=100, default='NA')
    air_france_created = models.BooleanField(default=False)
    air_france_password = models.CharField(
        max_length=32, validators=[any_or_na], default='NA'
    )
    aeromexico_created = models.BooleanField(default=False)
    aeromexico_password = models.CharField(
        max_length=32, validators=[any_or_na], default='NA'
    )
    avianca_created = models.BooleanField(default=False)
    avianca_password = models.CharField(
        max_length=32, validators=[any_or_na], default='NA'
    )
    korean_air_created = models.BooleanField(default=False)
    korean_air_password = models.CharField(
        max_length=32, validators=[any_or_na], default='NA'
    )
    china_airlines_created = models.BooleanField(default=False)
    china_airlines_password = models.CharField(
        max_length=32, validators=[any_or_na], default='NA'
    )
    recovery_email = models.EmailField(max_length=150)
    email_forwarding = models.BooleanField(default=False)
    auto_po_seats_scouts = models.BooleanField(default=False)
    errors_failed = models.CharField(max_length=255, validators=[any_or_na])
    tm_created = models.BooleanField(default=False)
    tm_password = models.CharField(max_length=32, validators=[any_or_na])
    tm_address = models.CharField(max_length=255, validators=[any_or_na], default='NA')
    axs_created = models.BooleanField(default=False)
    axs_password = models.CharField(max_length=32, validators=[any_or_na])
    sg_created = models.BooleanField(default=False)
    sg_password = models.CharField(max_length=32, validators=[any_or_na])
    tickets_com_created = models.BooleanField(default=False)
    facebook_created = models.BooleanField(default=False)
    twitter_created = models.BooleanField(default=False)
    eventbrite = models.BooleanField(default=False)
    etix = models.BooleanField(default=False)
    ticket_web = models.BooleanField(default=False)
    big_tickets = models.BooleanField(default=False)
    amazon = models.BooleanField(default=False)
    secondary_password = models.CharField(max_length=32, validators=[any_or_na])
    seat_scouts_added = models.BooleanField(default=False)
    seat_scouts_status = models.BooleanField(default=False)
    team = models.CharField(max_length=255, validators=[any_or_na])
    specific_team = models.CharField(max_length=255, validators=[any_or_na])
    forward_to = models.CharField(max_length=150, validators=[any_or_na])
    forward_email_password = models.CharField(max_length=32, validators=[any_or_na])
    seat_scouts_password = models.CharField(max_length=32, validators=[any_or_na])
    password_matching = models.BooleanField(default=False)
    disabled = models.BooleanField(default=False)
    created_by = models.CharField(
        max_length=32, validators=[any_or_na], default='MATEEN'
    )
    edited_by = models.CharField(max_length=32, validators=[any_or_na], default='NA')
    ld_computer_used = models.CharField(max_length=50, validators=[any_or_na])
    created_at = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    last_opened = models.DateField(null=True, blank=True)
    comments = models.TextField(validators=[any_or_na])
    phone = models.CharField(max_length=50, validators=[any_or_na], default='NA')
    tickets_com_password = models.CharField(
        max_length=50, validators=[any_or_na], default='NA'
    )
    password_reset = models.BooleanField(default=False)
    active_tickets_inside = models.BooleanField(default=False)
    migrated_from = models.CharField(
        max_length=100, validators=[any_or_na], default='NA'
    )
    migrated_to = models.CharField(max_length=100, validators=[any_or_na], default='NA')
    history = HistoricalRecords()

    def __str__(self):
        return self.email

    class Meta:
        db_table = "content\".\"accounts"
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        ordering = ['-created_at']
        permissions = (
            ('import_accounts', 'Can import'),
            ('export_accounts', 'Can export'),
        )
        # indexes = [
        #     models.Index(fields=('last_name', 'first_name',), name='accounts_last_first_name_idx'),
        #     models.Index(fields=('email',), name='accounts_email_idx'),
        #     models.Index(fields=('last_opened',), name='accounts_last_opened_idx'),
        # ]

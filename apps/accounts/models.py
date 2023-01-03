from django.db import models
from django.contrib.auth import get_user_model

from apps.cards.validators import any_or_na

User = get_user_model()


class Accounts(models.Model):
    """Table that contains all company's accounts"""

    first_name = models.CharField(max_length=100, validators=[any_or_na])
    last_name = models.CharField(max_length=100, validators=[any_or_na])
    email = models.EmailField(max_length=150, db_index=True)
    type = models.CharField(max_length=100, validators=[any_or_na])
    password = models.CharField(max_length=32, validators=[any_or_na])
    recovery_email = models.EmailField(max_length=150)
    email_forwarding = models.BooleanField(default=False)
    auto_po_seats_scouts = models.BooleanField(default=False)
    errors_failed = models.CharField(max_length=255, validators=[any_or_na])
    tm_created = models.BooleanField(default=False)
    tm_password = models.CharField(max_length=32, validators=[any_or_na])
    axs_created = models.BooleanField(default=False)
    axs_password = models.CharField(max_length=32, validators=[any_or_na])
    sg_created = models.BooleanField(default=False)
    sg_password = models.CharField(max_length=32, validators=[any_or_na])
    tickets_com_created = models.BooleanField(default=False)
    eventbrite = models.BooleanField(default=False)
    etix = models.BooleanField(default=False)
    ticket_web = models.BooleanField(default=False)
    big_tickets = models.BooleanField(default=False)
    amazon = models.BooleanField(default=False)
    secondary_password = models.CharField(max_length=32, validators=[any_or_na])
    seat_scouts_added = models.BooleanField(default=False)
    seat_scouts_status = models.BooleanField(default=False)
    airfrance = models.BooleanField(default=False)
    team = models.CharField(max_length=255, validators=[any_or_na])
    specific_team = models.CharField(max_length=255, validators=[any_or_na])
    forward_to = models.CharField(max_length=150, validators=[any_or_na])
    forward_email_password = models.CharField(max_length=32, validators=[any_or_na])
    disabled = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL,
                                   related_name='created_by_accounts_set', null=True)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL,
                                  related_name='edited_by_accounts_set', null=True)
    ld_computer_used = models.CharField(max_length=50, validators=[any_or_na])
    created_at = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    last_opened = models.DateField(null=True, blank=True)
    comments = models.TextField(validators=[any_or_na])

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        ordering = ['-created_at']
        permissions = (('import_accounts', 'Can import'), ('export_accounts', 'Can export'))

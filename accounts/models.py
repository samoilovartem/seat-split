from django.db import models


class Accounts(models.Model):
    full_name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=150, db_index=True, null=True, blank=True)
    password = models.CharField(max_length=32, null=True, blank=True)
    email_provider = models.EmailField(max_length=150, db_index=True, null=True, blank=True)
    forward_email = models.EmailField(max_length=150, db_index=True, null=True, blank=True)
    forward_email_password = models.CharField(max_length=32, null=True, blank=True)
    email_forwarding = models.BooleanField(default=False)
    auto_po_seats_scouts = models.BooleanField(default=False)
    errors_failed = models.CharField(max_length=255, null=True, blank=True)
    seat_scouts_added = models.BooleanField(default=False)
    seat_scouts_status = models.BooleanField(default=False)
    seat_scouts_password = models.CharField(max_length=32, null=True, blank=True)
    password_matching = models.BooleanField(default=False)
    team = models.CharField(max_length=255, null=True, blank=True)
    tm_address = models.CharField(max_length=255, null=True, blank=True)
    tm_password = models.CharField(max_length=32, null=True, blank=True)
    axs_password = models.CharField(max_length=32, null=True, blank=True)
    sg_password = models.CharField(max_length=32, null=True, blank=True)
    in_tickets_com = models.BooleanField(default=False)
    eventbrite = models.BooleanField(default=False)
    etix = models.BooleanField(default=False)
    ticket_web = models.BooleanField(default=False)
    big_tickets = models.BooleanField(default=False)
    amazon = models.BooleanField(default=False)
    secondary_password = models.CharField(max_length=32, null=True, blank=True)
    is_disabled = models.BooleanField(default=False)
    ld_computer_used = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated')
    created_by = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        ordering = ['-created_at']


from django.db import models


class Accounts(models.Model):
    """Table that contains all company's accounts"""

    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=150, db_index=True, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=32, null=True, blank=True)
    recovery_email = models.EmailField(max_length=150, db_index=True, null=True, blank=True)
    email_forwarding = models.BooleanField(default=False)
    auto_po_seats_scouts = models.BooleanField(default=False)
    errors_failed = models.CharField(max_length=255, null=True, blank=True)
    tm_created = models.BooleanField(default=False)
    tm_password = models.CharField(max_length=32, null=True, blank=True)
    axs_created = models.BooleanField(default=False)
    axs_password = models.CharField(max_length=32, null=True, blank=True)
    sg_created = models.BooleanField(default=False)
    sg_password = models.CharField(max_length=32, null=True, blank=True)
    tickets_com_created = models.BooleanField(default=False)
    eventbrite = models.BooleanField(default=False)
    etix = models.BooleanField(default=False)
    ticket_web = models.BooleanField(default=False)
    big_tickets = models.BooleanField(default=False)
    amazon = models.BooleanField(default=False)
    secondary_password = models.CharField(max_length=32, null=True, blank=True)
    seat_scouts_added = models.BooleanField(default=False)
    seat_scouts_status = models.BooleanField(default=False)
    airfrance = models.BooleanField(default=False)
    team = models.CharField(max_length=255, null=True, blank=True)
    specific_team = models.CharField(max_length=255, null=True, blank=True)
    forward_to = models.EmailField(max_length=150, db_index=True, null=True, blank=True)
    forward_email_password = models.CharField(max_length=32, null=True, blank=True)
    disabled = models.BooleanField(default=False)
    created_by = models.CharField(max_length=50, null=True, blank=True)
    edited_by = models.CharField(max_length=50, null=True, blank=True)
    ld_computer_used = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    last_opened = models.DateField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        ordering = ['-created_at']
        permissions = (('import_accounts', 'Can import'), ('export_accounts', 'Can export'))

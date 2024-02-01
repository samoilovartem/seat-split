from uuid import uuid4

from simple_history.models import HistoricalRecords

from django.db import models
from django.db.models import UniqueConstraint
from django.utils.timezone import now

from apps.stt.models.ticket_holder import TicketHolder


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
        db_table = 'content"."ticket'
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

from uuid import uuid4

from django.db import models
from simple_history.models import HistoricalRecords

from apps.stt.models.ticket import Ticket


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
        db_table = 'content"."purchase'
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'

    def __str__(self):
        return f'{self.ticket}'

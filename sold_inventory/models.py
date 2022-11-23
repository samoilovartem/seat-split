from django.db import models


class MLBSoldInventory(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    in_hand_date = models.DateTimeField(null=True, blank=True)
    event_id = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.CharField(max_length=255, null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    section = models.CharField(max_length=50, null=True, blank=True)
    row = models.CharField(max_length=50, null=True, blank=True)
    cost = models.CharField(max_length=50, null=True, blank=True)
    face_value = models.CharField(max_length=50, null=True, blank=True)
    list_price = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    last_price_update = models.DateTimeField(null=True, blank=True)
    broadcast = models.CharField(max_length=100, null=True, blank=True)
    unit_cost_average = models.CharField(max_length=100, null=True, blank=True)
    invoice_id = models.CharField(max_length=255, null=True, blank=True)
    invoice_date = models.DateTimeField(null=True, blank=True)
    total = models.CharField(max_length=100, null=True, blank=True)
    fulfillment_status = models.CharField(max_length=100, null=True, blank=True)
    payment_status = models.CharField(max_length=100, null=True, blank=True)
    profit = models.CharField(max_length=100, null=True, blank=True)
    profit_margin = models.CharField(max_length=100, null=True, blank=True)
    vendor = models.CharField(max_length=100, null=True, blank=True)
    fulfillment_date = models.DateTimeField(null=True, blank=True)
    invoice_tags = models.CharField(max_length=255, null=True, blank=True)
    unit_ticket_sales = models.CharField(max_length=100, null=True, blank=True)
    event_name = models.CharField(max_length=255, null=True, blank=True)
    event_date = models.DateTimeField(null=True, blank=True)
    event_venue_name = models.CharField(max_length=100, null=True, blank=True)
    performer_name = models.CharField(max_length=100, null=True, blank=True)
    performer_category_name = models.CharField(max_length=100, null=True, blank=True)
    performer_category_type = models.CharField(max_length=100, null=True, blank=True)
    row_count = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    tag = models.CharField(max_length=100, null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True)
    customer = models.CharField(max_length=255, null=True, blank=True)
    invoice_status = models.CharField(max_length=255, null=True, blank=True)
    purchase_ids = models.CharField(max_length=255, null=True, blank=True)

    order_email = models.EmailField(max_length=150, db_index=True, null=True, blank=True)
    order_id = models.CharField(max_length=255, null=True, blank=True)
    purchased = models.BooleanField(default=False)
    po = models.BooleanField(default=False)
    filled = models.BooleanField(default=False)
    extra_tickets = models.CharField(max_length=255, null=True, blank=True)
    upgraded_section = models.CharField(max_length=255, null=True, blank=True)
    edited_by = models.CharField(max_length=100, null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f'Item {self.id}'

    class Meta:
        verbose_name = 'MLB Sold Inventory'
        verbose_name_plural = 'MLB Sold Inventories'
        ordering = ['-id']




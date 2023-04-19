from simple_history.models import HistoricalRecords

from django.contrib.auth import get_user_model
from django.db import models

from apps.cards.validators import (
    clean_card_number,
    clean_cvv_number,
    clean_expiration_date,
    clean_state,
    clean_zip_code,
)
from apps.utils.validators import any_or_na

User = get_user_model()


class Cards(models.Model):
    """Table that contains all company's cards"""

    account_assigned = models.EmailField(max_length=150, db_index=True)
    platform = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    parent_card = models.CharField(max_length=150, validators=[any_or_na])
    card_number = models.CharField(max_length=16, validators=[clean_card_number])
    expiration_date = models.CharField(max_length=5, validators=[clean_expiration_date])
    cvv_number = models.CharField(max_length=4, validators=[clean_cvv_number])
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='created_by_cards_set', null=True
    )
    team = models.CharField(max_length=20)
    specific_team = models.CharField(max_length=100, validators=[any_or_na])
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2, validators=[clean_state])
    zip_code = models.CharField(max_length=5, validators=[clean_zip_code])
    in_tm = models.BooleanField(default=False)
    in_tickets_com = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.account_assigned

    class Meta:
        db_table = "content\".\"cards"
        verbose_name = 'Card'
        verbose_name_plural = 'Cards'
        ordering = ['-created_at']
        unique_together = ['account_assigned', 'platform']
        permissions = (('import_cards', 'Can import'), ('export_cards', 'Can export'))

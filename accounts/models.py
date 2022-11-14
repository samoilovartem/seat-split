from django.db import models
from .validators import clean_card_number, clean_expiration_date, clean_cvv_number, clean_zip_code, clean_state
from django.db.models import UniqueConstraint


class Accounts(models.Model):
    """Table that contains all company's accounts"""

    account_assigned = models.EmailField(max_length=150, db_index=True, verbose_name='Account',
                                         null=True, blank=True)
    platform = models.CharField(max_length=255, verbose_name='Platform', null=True, blank=True)
    type = models.CharField(max_length=255, verbose_name='Type', null=True, blank=True)
    parent_card = models.CharField(max_length=150, verbose_name='Parent', null=True, blank=True)
    card_number = models.CharField(max_length=16, validators=[clean_card_number], blank=True)
    expiration_date = models.CharField(max_length=5, validators=[clean_expiration_date],
                                       verbose_name='Exp.date', null=True, blank=True)
    cvv_number = models.CharField(max_length=4, validators=[clean_cvv_number],
                                  verbose_name='CVV', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated')
    created_by = models.CharField(max_length=20, null=True, blank=True)
    team = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True,
                             validators=[clean_state])
    zip_code = models.CharField(max_length=5, null=True, blank=True,
                                validators=[clean_zip_code])
    in_tm = models.BooleanField(verbose_name='TM', default=False)
    in_tickets_com = models.BooleanField(verbose_name='tickets.com', default=False)

    def __str__(self):
        return self.account_assigned

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        ordering = ['-created_at']
        # constraints = [
        #     UniqueConstraint(
        #         fields=['account_assigned', 'platform'],
        #         name='email_and_platform_unique',
        #     ),
        # ]
        unique_together = ['account_assigned', 'platform']

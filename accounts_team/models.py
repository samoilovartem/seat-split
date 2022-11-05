from django.db import models
from .validators import clean_card_number, clean_expiration_date, clean_cvv_number, clean_limit
from django.db.models import UniqueConstraint


class Accounts(models.Model):
    account_assigned = models.EmailField(max_length=150, db_index=True, verbose_name='Account')
    platform = models.ForeignKey('Platform', on_delete=models.PROTECT)
    type = models.ForeignKey('Type', on_delete=models.PROTECT)
    parent_card = models.CharField(max_length=150, verbose_name='Parent')
    card_number = models.CharField(max_length=16, validators=[clean_card_number])
    expiration_date = models.CharField(max_length=5,
                                       validators=[clean_expiration_date],
                                       verbose_name='Exp.date')
    cvv_number = models.CharField(max_length=3,
                                  validators=[clean_cvv_number],
                                  verbose_name='CVV')
    limit = models.CharField(default='0', max_length=20, validators=[clean_limit])
    created_by = models.ForeignKey('Employees',
                                   on_delete=models.PROTECT,
                                   verbose_name='Responsible')
    team = models.ForeignKey('Teams', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated')
    in_tm = models.BooleanField(verbose_name='tickets.com')
    in_tickets_com = models.BooleanField(verbose_name='TM')

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


class Employees(models.Model):
    name = models.CharField(max_length=150, db_index=True, verbose_name='Employee name')
    team = models.ForeignKey('Teams',
                             on_delete=models.PROTECT,
                             related_name='employees',
                             related_query_name='employee')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        ordering = ['name']


class Teams(models.Model):
    name = models.CharField(max_length=150, db_index=True, verbose_name='Team name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
        ordering = ['name']


class Platform(models.Model):
    name = models.CharField(max_length=150, db_index=True, verbose_name='Platform')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Platform'
        verbose_name_plural = 'Platforms'
        ordering = ['name']


class Type(models.Model):
    name = models.CharField(max_length=150, db_index=True, verbose_name='Type')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Type'
        verbose_name_plural = 'Types'
        ordering = ['name']

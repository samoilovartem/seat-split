import re

from django.core.exceptions import ValidationError
from django.db import models


def clean_card_number(card_number):
    if not re.match(r'^[0-9]+$', card_number) or len(card_number) < 16:
        raise ValidationError('Card number must have 16 digits!')
    return card_number


def clean_expiration_date(expiration_date):
    if len(expiration_date) < 5:
        raise ValidationError('Expiration date must be in format MM/YY')
    if not re.match(r'^[/0-9]+$', expiration_date):
        raise ValidationError('Please use only digits!')
    if expiration_date[2] != '/':
        raise ValidationError('Expiration date must be in format MM/YY')
    if int(expiration_date[0]) >= 1 and int(expiration_date[0]) + int(expiration_date[1]) > 3:
        raise ValidationError('Wrong expiration month!')
    return expiration_date


def clean_cvv_number(cvv_number):
    if len(cvv_number) < 3:
        raise ValidationError('CVV number must have 3 digits!')
    if not re.match(r'^[0-9]+$', cvv_number):
        raise ValidationError('Please use only digits!')
    return cvv_number


class Accounts(models.Model):
    account_assigned = models.EmailField(max_length=150, unique=True, db_index=True)
    platform = models.CharField(max_length=150)
    type = models.CharField(max_length=150)
    parent_card = models.CharField(max_length=150)
    card_number = models.CharField(max_length=16, validators=[clean_card_number])
    expiration_date = models.CharField(max_length=5, validators=[clean_expiration_date])
    cvv_number = models.CharField(max_length=3, validators=[clean_cvv_number])
    created_by = models.ForeignKey('Employees', on_delete=models.PROTECT)
    team = models.ForeignKey('Teams', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # auto_now - saving every time we update something
    in_tm = models.BooleanField(verbose_name='Added in tickets.com')
    in_tickets_com = models.BooleanField(verbose_name='Added in TM')

    def __str__(self):
        return self.account_assigned

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        ordering = ['-created_at']


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


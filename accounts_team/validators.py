import re
from django.core.exceptions import ValidationError


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


def clean_limit(limit):
    if not re.match(r'^[0-9]+$', limit):
        raise ValidationError('Limit must be a number!')
    return limit
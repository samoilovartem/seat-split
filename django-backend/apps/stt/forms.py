from django import forms
from apps.stt.models import Ticket
from django.core.exceptions import ValidationError


class TicketAdminForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        listing_status = cleaned_data.get('listing_status')
        price = cleaned_data.get('price')
        if listing_status == 'Requested for delisting':
            raise ValidationError(
                'A ticket with listing status "Requested for delisting" cannot be saved. '
                'You must change the status first.'
            )
        if not price:
            raise ValidationError('A ticket must have a price.')
        return cleaned_data

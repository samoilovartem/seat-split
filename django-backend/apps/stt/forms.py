from django import forms
from django.core.exceptions import ValidationError

from apps.stt.models import Ticket


class TicketAdminForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        listing_status = cleaned_data.get('listing_status')
        if listing_status == 'Cancelled':
            raise ValidationError(
                'A ticket with listing status "Cancelled" cannot be saved. You must change the status first.'
            )
        return cleaned_data

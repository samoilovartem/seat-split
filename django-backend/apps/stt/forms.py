from django import forms
from django.core.exceptions import ValidationError

from apps.stt.models import Season, Ticket
from config.components.business_related import SUPPORTED_LEAGUES


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


class DataProcessorForm(forms.Form):
    json_file = forms.FileField()
    season = forms.ModelChoiceField(queryset=Season.objects.all())
    league = forms.ChoiceField(choices=((league, league) for league in SUPPORTED_LEAGUES))
    replacements = forms.CharField(
        widget=forms.Textarea,
        help_text="""The field, value of which you want to replace, should be the key.
        Provide replacements in this format:
        {
            "name": {
                "\\bSt Louis Cardinals\\b": "St. Louis Cardinals"
            }
        }
        Note: "\\b" is used to indicate a word boundary, ensuring the replacement
        only happens when the match is a whole word and not part of a larger word or phrase.""",
    )

from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import LawnsAccounts


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class AccountsForm(forms.ModelForm):

    class Meta:
        model = LawnsAccounts
        fields = ['account_assigned', 'platform', 'type', 'parent_card', 'card_number',
                  'expiration_date', 'cvv_number', 'in_tm']
        widgets = {
            'account_assigned': forms.TextInput(attrs={'class': 'form-control'}),
            'platform': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'parent_card': forms.TextInput(attrs={'class': 'form-control'}),
            'card_number': forms.TextInput(attrs={'class': 'form-control'}),
            'expiration_date': forms.TextInput(attrs={'class': 'form-control'}),
            'cvv_number': forms.TextInput(attrs={'class': 'form-control'}),
            'in_tm': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


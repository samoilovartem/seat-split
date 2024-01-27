from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.users.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower()
        if not email:
            raise forms.ValidationError('The email field cannot be blank.')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'The email {email} is already in use.')
        return email

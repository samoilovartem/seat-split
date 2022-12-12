from django import forms


class CardsForm(forms.ModelForm):
    def clean(self):
        cleaned_data = self.cleaned_data
        specific_team = cleaned_data.get('specific_team')
        if not specific_team or len(specific_team) < 2:
            raise forms.ValidationError("If SPECIFIC TEAM is not applicable to you, "
                                        "please input NA")
        if len(specific_team) == 2 and specific_team != 'NA':
            raise forms.ValidationError("If SPECIFIC TEAM is not applicable to you, "
                                        "please input NA")
        super(CardsForm, self).clean()
        return cleaned_data

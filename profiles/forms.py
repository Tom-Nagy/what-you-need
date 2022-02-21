''' Create and configure the profile form '''

from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    ''' Configure the profile form '''
    class Meta:
        ''' Form meta properties '''
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        '''
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        '''
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_full_name': 'Full Name',
            'default_email': 'Email Address',
            'default_phone_number': 'Phone Number',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_county_or_region': 'County or Region',
        }

        self.fields['default_full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'custom-form-input'
            self.fields[field].label = False

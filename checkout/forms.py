''' Create and configure the checkout form '''

from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    ''' Configure the order form '''
    class Meta:
        ''' Form meta properties '''
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2', 'postcode',
                  'town_or_city', 'county_or_region', 'country',)

    def __init__(self, *args, **kwargs):
        '''
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        '''
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'county_or_region': 'County or Region',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False

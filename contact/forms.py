'''Create and configure the product and review form'''

from django import forms

from .models import ContactUs


class ContactUsForm(forms.ModelForm):
    '''Configure the contact uc form '''
    class Meta:
        ''' Form meta properties '''
        model = ContactUs
        fields = ('subject', 'sender', 'body',)

    def __init__(self, *args, **kwargs):
        '''
        Add placeholders and classes and remove auto-generated labels
        '''
        super().__init__(*args, **kwargs)
        placeholders = {
            'sender': 'Your email address',
            'body': 'Sending us as much information as you can '
                    'would be a great help for us...',
        }

        for field in self.fields:
            if field != 'subject':
                placeholder = f'{placeholders[field]} *'
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'custom-form-input'
            self.fields[field].label = False

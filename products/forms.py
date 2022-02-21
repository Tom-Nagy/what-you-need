'''Create and configure the product and review form'''

from django import forms
from .widgets import CustomClearableFileInput

from .models import Product, Category, ProductReview


class ProductForm(forms.ModelForm):
    '''Configure the product form to add/edit products'''
    class Meta:
        ''' Form meta properties '''
        model = Product
        fields = '__all__'

    # Replace the image field the the custom widget
    image = forms.ImageField(label='Image',
                             required=False,
                             widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Replace the categorie select box to see the friendly name.
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        self.fields['category'].choices = friendly_names

        # Add custom class to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'custom-form-input'


class ProductReviewForm(forms.ModelForm):
    '''Configure the review form '''
    class Meta:
        ''' Form meta properties '''
        model = ProductReview
        fields = ('review_rating', 'content',)

    def __init__(self, *args, **kwargs):
        '''
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        '''
        super().__init__(*args, **kwargs)

        placeholders = {
            'content': 'Tell other customer what you think ...',
        }

        for field in self.fields:
            if field != 'review_rating':
                placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'custom-form-input'
            self.fields[field].label = False

'''Create and configure the products form'''

from django import forms
from .widgets import CustomClearableFileInput

from .models import Product, Category


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
            field.widget.attrs['class'] = 'product-form-input'

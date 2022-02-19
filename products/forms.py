'''Create and configure the products form'''

from django import forms

from .models import Product, Category


class ProductForm(forms.ModelForm):
    '''Configure the product form to add/edit products'''
    class Meta:
        ''' Form meta properties '''
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'product-form-input'

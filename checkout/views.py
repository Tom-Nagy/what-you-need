''' Views to manage and render the checkout pages '''
from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    '''
    View to display the checkout page including order summary and ckeout form
    '''
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, 'There is nothing in your bag at the moment')
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51JjLdoC2lzatXFr8OZNmxgrNw2sD4pE0A6JooNdhMDVgKEHuq6x4svncuT63BLVnDqFuM4AfklP3vWHxMDoO7WXR003Ji0Byjj',
        'client_secret': 'test client secret lol',
    }

    return render(request, template, context)

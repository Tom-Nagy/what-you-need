'''
Context processor to make bag contents available across the entire application.
'''
from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):
    '''
    Provide the content of the shopping bag with delivery cost and grand total
    '''

    bag_items = []
    total = 0
    product_count = 0
    free_products_count = 0
    free_products_list = []
    free_products = []
    free_product_threshold = 0
    bag = request.session.get('bag', {})

    for item_id, quantity in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        total += quantity * product.price
        product_count += quantity
        product_subtotal = quantity * product.price

        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
            'product_subtotal': product_subtotal
        })

    # Get a list of product price(s) to discount.
    if product_count % 3 == 0 and product_count != 0:
        free_products_count = int(product_count / 3)
        for items in bag_items:
            free_products_list += items.price
        free_products_list.sort()
        for product_prices in range(free_products_count):
            free_products += free_products_list.pop([0])
    elif product_count < 3:
        free_product_threshold = 3 - product_count
    else:
        free_product_threshold = product_count - (int(product_count / 3) * 3)

    delivery_cost = total * Decimal(settings.DELIVERY_COST / 100)
    grand_total = total = delivery_cost

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery_cost': delivery_cost,
        'free_products': free_products,
        'grand_total': grand_total,
        'free_product_threshold': free_product_threshold,
    }
    return context

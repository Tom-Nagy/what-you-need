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
    products_price_list = []
    free_products = []
    free_product_threshold = 0
    bag = request.session.get('bag', {})

    for item_id, quantity in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        total += quantity * product.price
        product_count += quantity
        product_subtotal = quantity * product.price
        for prices in range(quantity):
            products_price_list.append(float(product.price))

        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
            'product_subtotal': product_subtotal,
        })
    products_price_list.sort()

    # Every 3 items purchase the least expensive is offered.
    # Get the list of product prices and return a list of prices to discount 
    # and number of items to purchase for the next discount.
    if product_count % 3 == 0 and product_count != 0:
        free_products_count = int(product_count / 3)
        # Sorted() method from [venpa](https://stackoverflow.com/questions/
        # 22117834/how-do-i-return-a-list-of-the-3-lowest-values-in-another-list)
        free_products = sorted(products_price_list)[:free_products_count]
        free_product_threshold = 3
    elif product_count < 3:
        free_product_threshold = 3 - product_count
    else:
        free_products_count = int(product_count / 3)
        free_products = sorted(products_price_list)[:free_products_count]
        free_product_threshold = 3 - (
                                product_count - (free_products_count * 3))

    # Calculate the total discount
    discount = 0
    for prod in free_products:
        discount += Decimal(prod)

    # Calculate delivery cost and grand total
    delivery_cost = total * Decimal(settings.DELIVERY_COST / 100)
    grand_total = total + delivery_cost - discount

    # print(f'product count : {product_count}')
    # print(f'free threshold : {free_product_threshold}')
    # print(f'product price list : {products_price_list}')
    # print(f'free products : {free_products}')
    # print(f'discount : {discount}')

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery_cost': delivery_cost,
        'free_products': free_products,
        'discount': discount,
        'grand_total': grand_total,
        'free_product_threshold': free_product_threshold,
    }
    return context

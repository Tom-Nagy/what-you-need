''' Custom template filter for checkout '''
from django import template

register = template.Library()


@register.filter(name='calc_price_sale_item')
def calc_price_sale_item(quantity, lineitem_total):
    ''' Calculate the price of an on sale item '''
    return lineitem_total / quantity

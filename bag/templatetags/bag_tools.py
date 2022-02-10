''' Custom template filter '''
from django import template

register = template.Library()


@register.filter(name='calc_max_value')
def calc_max_value(available_quantity, bag_item_quantity):
    ''' Calculate the maximum value input '''
    return available_quantity + bag_item_quantity

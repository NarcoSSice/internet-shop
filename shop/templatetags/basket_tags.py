from django import template

register = template.Library()


@register.simple_tag()
def check_item_in_basket(basket, product_id):
    if basket:
        for item in basket:
            if item['product_id'] == str(product_id):
                return True
    return False


@register.simple_tag()
def item_quantity(basket, product_id):
    if basket:
        for item in basket:
            if item['product_id'] == str(product_id):
                return item['quantity']
    return False


@register.simple_tag()
def calculate_price(price, quantity):
    return int(price) * quantity

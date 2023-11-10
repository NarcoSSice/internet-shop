from django import template

from shop.models import Product

register = template.Library()


@register.simple_tag()
def get_product_by_category(category_id=None):
    products = Product.objects.filter(subcategory=category_id)[:4]
    return products

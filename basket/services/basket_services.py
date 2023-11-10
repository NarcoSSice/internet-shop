from django.shortcuts import get_object_or_404

from shop.models import Product


def add_item_to_basket(request, product_id):
    exist_product = next((item for item in request.session['basket'] if item['product_id'] == product_id), False)

    add_data = {
        'product_id': product_id,
    }

    if not exist_product:
        request.session['basket'].append(add_data)
        request.session.modified = True


def remove_item_from_basket(request, product_id):
    exist_product = next((item for item in request.session['basket'] if item['product_id'] == product_id), False)

    if exist_product:
        request.session['basket'].remove(exist_product)

    if not request.session.get('basket'):
        del request.session['basket']


def create_basket_list(request):
    products = []
    if request.session.get('basket'):
        for item in request.session.get('basket'):
            product = get_object_or_404(Product, pk=item['product_id'])
            products.append(product)

    return products

import json

from django.shortcuts import get_object_or_404

from shop.models import Product


def add_item_to_basket(request, product_id):
    exist_product = next((item for item in request.session['basket'] if item['product_id'] == product_id), False)

    add_data = {
        'product_id': str(product_id),
        'quantity': 1,
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
    basket = request.session.get('basket')
    if basket:
        for item in basket:
            product = get_object_or_404(Product, pk=item['product_id'])
            products.append(product)

    return products


def change_product_quantity(request):
    data = json.loads(request.body)
    product_id = str(data.get('product_id'))
    new_quantity = data.get('new_quantity')

    item = next((item for item in request.session['basket'] if item['product_id'] == product_id), None)
    if item:
        item['quantity'] = new_quantity
        request.session.modified = True

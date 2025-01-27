import uuid

from shop.models import Order, OrderItem, Product


def create_basket_order(user):
    order = Order.objects.create(
        customer=user,
        transaction_id=int(uuid.uuid4())
    )
    return order


def create_order_items(basket, order):
    for item in basket:
        product = Product.objects.get(id=int(item['product_id']))
        OrderItem.objects.create(
            product=product,
            order=order,
        )


def create_order_context(request):
    total_price = 0
    total_quantity = 0
    basket = request.session['basket']
    for item in basket:
        product = Product.objects.get(id=int(item['product_id']))
        price = product.price * item['quantity']
        total_price += price
        total_quantity += item['quantity']
    return_context = {
        'total_price': total_price,
        'products_quantity': total_quantity,
    }
    return return_context

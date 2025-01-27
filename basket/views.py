from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect

from basket.services.basket_services import add_item_to_basket, remove_item_from_basket, create_basket_list, \
    change_product_quantity


def basket_list(request):
    products = create_basket_list(request)
    paginator = Paginator(products, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'basket/basket.html', context=context)


def add_basket_item(request, product_id):
    if request.method == 'POST':
        if not request.session.get('basket'):
            request.session['basket'] = list()

        add_item_to_basket(request, product_id)
    return redirect(request.POST.get('url_from'))


def remove_basket_item(request, product_id):
    if request.method == 'POST':
        remove_item_from_basket(request, product_id)
        request.session.modified = True
    return redirect(request.POST.get('url_from'))


def clear_basket(request):
    if request.session.get('basket'):
        del request.session['basket']

    return redirect('basket_list')


def update_product_quantity(request):
    if request.method == 'POST':
        change_product_quantity(request)
    return JsonResponse({'success': True})

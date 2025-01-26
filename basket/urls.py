from django.urls import path

from basket.views import basket_list, add_basket_item, remove_basket_item, clear_basket, update_product_quantity

urlpatterns = [
    path('', basket_list, name='basket_list'),
    path('update_quantity/', update_product_quantity, name='update_quantity'),
    path('<product_id>/add/', add_basket_item, name='add_basket_item'),
    path('<product_id>/remove/', remove_basket_item, name='remove_basket_item'),
    path('clear/', clear_basket, name='clear_basket'),
]

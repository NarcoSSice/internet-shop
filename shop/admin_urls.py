from django.urls import path

from .views import generate_product_price_view, generate_product_description_view,generate_product_image_view

urlpatterns = [
    path('generate_description/', generate_product_description_view, name='generate_description'),
    path('generate_price/', generate_product_price_view, name='generate_price'),
    path('generate_image/', generate_product_image_view, name='generate_image'),
]

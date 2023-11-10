from django.urls import path

from shop.views import index, RegisterView, register_confirm, LoginUser, logout_customer, show_subcategories, \
    show_subcategory_products, show_products

urlpatterns = [
    path('', index, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/<token>', register_confirm, name='register_confirm'),
    path('login/', LoginUser.as_view(), name='my_login'),
    path('logout/', logout_customer, name='my_logout'),

    path('<category_slug>/', show_subcategories, name='show_subcategories'),
    path('<category_slug>/<subcategory_slug>', show_subcategory_products, name='show_subcategory_products'),
    path('<category_slug>/<subcategory_slug>/<product_slug>', show_products, name='show_product_details')
]

from django.urls import path, include

from .views import (ProductViewSet, SubCategoryViewSet, CategoryViewSet,
                    OrderItemListCreateView, OrderItemRetrieveDestroyView,
                    OrderListView, OrderRetrieveUpdateDestroyView,
                    ShippingRetrieveUpdateView, ShippingCreateListView, CustomerListView,
                    CustomerRetrieveUpdateDestroyView, CreateCustomer, ConfirmCustomerView, BasketListView,
                    AddUpdateRemoveBasketItem)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'subcategories', SubCategoryViewSet, basename='subcategory')
router.register(r'categories', CategoryViewSet, basename='category')


urlpatterns = [
    path('', include(router.urls)),
    path('orderitems/', OrderItemListCreateView.as_view()),
    path('orderitems/<int:pk>/', OrderItemRetrieveDestroyView.as_view()),
    path('orders/', OrderListView.as_view()),
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroyView.as_view()),
    path('shippings/', ShippingCreateListView.as_view()),
    path('shippings/<int:pk>/', ShippingRetrieveUpdateView.as_view()),
    path('users/', CustomerListView.as_view()),
    path('users/<int:pk>/', CustomerRetrieveUpdateDestroyView.as_view()),
    path('createuser/', CreateCustomer.as_view()),
    path('auth/confirm/<str:token>/', ConfirmCustomerView.as_view(), name='api_register_confirm'),
    path('drf-auth/', include('rest_framework.urls')),

    path('basketlist/', BasketListView.as_view()),
    path('basket-item/<int:product_id>/', AddUpdateRemoveBasketItem.as_view()),
]

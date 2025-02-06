import json

from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from basket.services.basket_services import create_basket_list, remove_item_from_basket, add_item_to_basket
from basket.views import clear_basket
from shop.models import Product, SubCategory, Category, OrderItem, Order, Shipping, Customer
from shop.services.auth_services import confirm_customer
from .permissions import IsAdminUserOrReadOnly, IsAdminUserOrIsOwnerReadDestroyOnly, IsAdminUserOrIsOwnerReadUpdate, \
    IsAdminUserOrIsAuthenticatedCreateOnly, IsAdminUserOrIsOwner
from .serializers import ProductSerializer, SubCategorySerializer, CategorySerializer, OrderItemSerializer, \
    OrderSerializer, ShippingSerializer, CustomerSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUserOrReadOnly, )


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = (IsAdminUserOrReadOnly, )


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly, )


class OrderItemListCreateView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = (IsAdminUser,)


class OrderItemRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = (IsAdminUser, )


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAdminUser,)


class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAdminUserOrIsOwnerReadDestroyOnly, )


class ShippingCreateListView(generics.ListCreateAPIView):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer
    permission_classes = (IsAdminUserOrIsAuthenticatedCreateOnly, )


class ShippingRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer
    permission_classes = (IsAdminUserOrIsOwnerReadUpdate, )


class CustomerListView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (IsAdminUser, )


class CustomerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (IsAdminUserOrIsOwner, )


class CreateCustomer(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class ConfirmCustomerView(APIView):

    def get(self, request, token):
        if confirm_customer(token):
            return Response({"message": "Акаунт успішно активовано!"}, status=status.HTTP_200_OK)
        return Response({"error": "Невірний або застарілий токен, "
                        "новий токен підтвердження було надіслано на пошту"},
                        status=status.HTTP_400_BAD_REQUEST)


class BasketListView(APIView):

    def get(self, request):
        products = create_basket_list(request)
        serialized_products = ProductSerializer(products, many=True)

        return Response({'basket': serialized_products.data})

    def delete(self, request):
        clear_basket(request)

        return Response({'message': 'Кошик очищено!'}, status=status.HTTP_200_OK)


class AddUpdateRemoveBasketItem(APIView):

    def get(self, request, product_id):
        return Response({'basket': request.session.get('basket')})

    def post(self, request, product_id):
        if not request.session.get('basket'):
            request.session['basket'] = list()

        add_item_to_basket(request, product_id)
        return Response({'message': 'Товар додано в кошик'}, status=status.HTTP_200_OK)

    def put(self, request, product_id):
        data = json.loads(request.body)
        new_quantity = data.get('new_quantity')

        item = next((item for item in request.session['basket'] if item['product_id'] == str(product_id)), None)
        if item:
            item['quantity'] = new_quantity
            request.session.modified = True
        return Response({'message': 'Кількість товару змінено'}, status=status.HTTP_200_OK)

    def delete(self, request, product_id):
        remove_item_from_basket(request, product_id)
        request.session.modified = True
        return Response({'message': 'Товар видалено з кошику'}, status=status.HTTP_200_OK)


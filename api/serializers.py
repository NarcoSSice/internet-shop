from rest_framework import serializers

from shop.models import Product, SubCategory, Category, OrderItem, Order, Shipping, Customer
from shop.services.auth_services import send_email_confirmation
from shop.services.order_services import create_basket_order, create_order_items
from .mixins import SlugMixin


class ProductSerializer(SlugMixin, serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'slug', 'description', 'price', 'image', 'subcategory')
        read_only_fields = ('slug', )


class SubCategorySerializer(SlugMixin, serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('name', 'slug', 'super_category')
        read_only_fields = ('slug', )


class CategorySerializer(SlugMixin, serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug', )
        read_only_fields = ('slug', )


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('time_create', 'transaction_id', )


class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = '__all__'
        read_only_fields = ('customer', 'order', 'date')

    def create(self, validated_data):
        request = self.context['request']
        basket = request.session.get('basket')

        order = create_basket_order(request.user)
        create_order_items(basket, order)

        shipping = Shipping.objects.create(
            customer=request.user,
            order=order,
            **validated_data
        )

        return shipping


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ('username', 'groups', 'user_permissions', )
        read_only_fields = ('is_staff', 'is_active', 'date_joined', 'is_superuser',
                            'last_login', 'is_staff', 'is_active', 'date_joined')

        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        customer = Customer(**validated_data)
        customer.set_password(validated_data['password'])
        customer.save()
        send_email_confirmation(self.context.get('request'), customer, is_api=True)
        return customer

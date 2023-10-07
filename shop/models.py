from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class Customer(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='URL')

    class Meta:
        db_table = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('', kwargs={'category_slug': self.slug})


class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='URL')
    super_category = models.ForeignKey(Category, on_delete=models.PROTECT)

    class Meta:
        db_table = 'SubCategories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('', kwargs={'subcategory_slug': self.slug})


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField()
    price = models.FloatField()
    # image = models.ImageField()
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT)

    class Meta:
        db_table = 'Products'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('', kwargs={'product_slug': self.slug})


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    time_create = models.DateTimeField(auto_now_add=True)
    transaction_id = models.IntegerField()

    class Meta:
        db_table = 'Orders'

    def __str__(self):
        return f'Order number: {self.pk}, status: {self.status}'


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        db_table = 'OrderItems'


class Shipping(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Shippings'

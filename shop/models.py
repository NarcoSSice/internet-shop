from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class CustomerManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class Customer(AbstractUser):
    username = models.CharField(
        _("username"),
        max_length=150,
        null=True,
        blank=True
    )

    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    phone = models.CharField(_("phone"), max_length=20, blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = CustomerManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'User {self.email}'


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='URL')

    class Meta:
        db_table = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('show_subcategories', kwargs={'category_slug': self.slug})


class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='URL')
    super_category = models.ForeignKey(Category, on_delete=models.PROTECT)

    class Meta:
        db_table = 'SubCategories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('show_subcategory_products', kwargs={'category_slug': self.super_category.slug,
                                                            'subcategory_slug': self.slug})


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='images/%Y/%m/%d/', null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT)

    class Meta:
        db_table = 'Products'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('show_product_details', kwargs={
            'category_slug': self.subcategory.super_category.slug,
            'subcategory_slug': self.subcategory.slug,
            'product_slug': self.slug,
                                   })


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    time_create = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100)

    class Meta:
        db_table = 'Orders'

    def __str__(self):
        return f'Order number: {self.pk}, status: {self.status}'


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, null=True, blank=True)

    class Meta:
        db_table = 'OrderItems'

    def __str__(self):
        return f'Product: {self.product.name}; Order number: {self.order.id}'


class Shipping(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Shippings'

    def __str__(self):
        return f'Order number: {self.order.id}; status: {self.order.status}'

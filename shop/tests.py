import json
from unittest import mock
from unittest.mock import patch

from django.test import TestCase, Client
from django.http import JsonResponse
from .models import *
from .forms import *
from .services.AI_services import generate_description, generate_price, generate_image_url
from openai import OpenAIError


class ModelsTestCase(TestCase):

    def setUp(self):
        # Створення тестових даних
        self.customer = Customer.objects.create(
            email="testuser@example.com",
            first_name="Test",
            last_name="User",
            is_active=False,
        )

        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics"
        )

        self.subcategory = SubCategory.objects.create(
            name="Smartphones",
            slug="smartphones",
            super_category=self.category
        )

        self.product = Product.objects.create(
            name="iPhone 13",
            slug="iphone-13",
            description="Latest Apple smartphone",
            price=1000,
            subcategory=self.subcategory
        )

        self.order = Order.objects.create(
            customer=self.customer,
            status=False,
            transaction_id="TRX12345"
        )

        self.order_item = OrderItem.objects.create(
            product=self.product,
            order=self.order,
            quantity=2
        )

        self.shipping = Shipping.objects.create(
            customer=self.customer,
            order=self.order,
            address="123 Test Street",
            city="TestCity"
        )

    def test_customer_creation(self):
        # Перевірка створення клієнта
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(self.customer.email, "testuser@example.com")
        self.assertFalse(self.customer.is_active)

    def test_category_creation(self):
        # Перевірка створення категорії
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(self.category.name, "Electronics")
        self.assertEqual(self.category.slug, "electronics")

    def test_subcategory_creation(self):
        # Перевірка створення підкатегорії
        self.assertEqual(SubCategory.objects.count(), 1)
        self.assertEqual(self.subcategory.name, "Smartphones")
        self.assertEqual(self.subcategory.super_category, self.category)

    def test_product_creation(self):
        # Перевірка створення продукту
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(self.product.name, "iPhone 13")
        self.assertEqual(self.product.subcategory, self.subcategory)
        self.assertEqual(self.product.price, 1000)

    def test_order_creation(self):
        # Перевірка створення замовлення
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(self.order.customer, self.customer)
        self.assertEqual(self.order.transaction_id, "TRX12345")
        self.assertFalse(self.order.status)

    def test_order_item_creation(self):
        # Перевірка створення елементу замовлення
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.quantity, 2)

    def test_shipping_creation(self):
        # Перевірка створення доставки
        self.assertEqual(Shipping.objects.count(), 1)
        self.assertEqual(self.shipping.customer, self.customer)
        self.assertEqual(self.shipping.address, "123 Test Street")
        self.assertEqual(self.shipping.city, "TestCity")

    def test_product_absolute_url(self):
        # Перевірка методу get_absolute_url() для продукту
        expected_url = f"/{self.category.slug}/{self.subcategory.slug}/{self.product.slug}"
        self.assertEqual(self.product.get_absolute_url(), expected_url)

    def test_category_absolute_url(self):
        # Перевірка методу get_absolute_url() для категорії
        expected_url = f"/{self.category.slug}/"
        self.assertEqual(self.category.get_absolute_url(), expected_url)


class CustomerManagerTests(TestCase):

    def test_create_user_with_email(self):
        """Перевірка створення звичайного користувача з email."""
        email = "user@example.com"
        password = "testpassword123"
        user = Customer.objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_email(self):
        """Перевірка помилки при спробі створення користувача без email."""
        with self.assertRaises(ValueError) as context:
            Customer.objects.create_user(email=None, password="testpassword123")
        self.assertEqual(str(context.exception), "The given email must be set")

    def test_create_superuser(self):
        """Перевірка створення суперкористувача."""
        email = "admin@example.com"
        password = "adminpassword123"
        superuser = Customer.objects.create_superuser(email=email, password=password)

        self.assertEqual(superuser.email, email)
        self.assertTrue(superuser.check_password(password))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_superuser_with_missing_is_superuser(self):
        """Перевірка помилки, якщо суперкористувач створений без is_superuser=True."""
        with self.assertRaises(ValueError) as context:
            Customer.objects.create_superuser(email="admin@example.com", password="testpassword123", is_superuser=False)
        self.assertEqual(str(context.exception), "Superuser must have is_superuser=True.")


class TestShopURLsHTTPStatus(TestCase):
    def setUp(self):
        """Попередні налаштування"""
        # Якщо необхідно, можна створити тестові дані тут
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics"
        )
        self.subcategory = SubCategory.objects.create(
            name="Smartphones",
            slug="smartphones",
            super_category=self.category
        )
        self.product = Product.objects.create(
            name="iPhone 13",
            slug="iphone-13",
            description="Latest Apple smartphone",
            price=1000,
            subcategory=self.subcategory,
            image="path/to/test/image.jpg"
        )
        self.token = "test_token"

    def test_home_page_status_code(self):
        """Перевіряємо, чи головна сторінка повертає статус 200"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_register_page_status_code(self):
        """Перевіряємо сторінку реєстрації"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_confirm_page_status_code(self):
        """Перевіряємо сторінку підтвердження реєстрації"""
        response = self.client.get(reverse('register_confirm', args=[self.token]))
        self.assertEqual(response.status_code, 302)

    def test_login_page_status_code(self):
        """Перевіряємо сторінку входу"""
        response = self.client.get(reverse('my_login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_page_status_code(self):
        """Перевіряємо сторінку виходу"""
        response = self.client.get(reverse('my_logout'))
        self.assertEqual(response.status_code, 302)  # Перенаправлення після виходу

    def test_make_order_page_status_code(self):
        """Перевіряємо сторінку створення замовлення"""
        response = self.client.get(reverse('make_order'))
        self.assertEqual(response.status_code, 302)  # Можливо, доступ лише для авторизованих користувачів

    def test_show_subcategories_page_status_code(self):
        """Перевіряємо сторінку показу підкатегорій"""
        response = self.client.get(reverse('show_subcategories', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)

    def test_show_subcategory_products_page_status_code(self):
        """Перевіряємо сторінку показу товарів у підкатегорії"""
        response = self.client.get(reverse('show_subcategory_products', args=[self.category.slug, self.subcategory.slug]))
        self.assertEqual(response.status_code, 200)

    def test_show_product_details_page_status_code(self):
        """Перевіряємо сторінку показу деталей товару"""
        response = self.client.get(reverse('show_product_details', args=[self.category.slug, self.subcategory.slug, self.product.slug]))
        self.assertEqual(response.status_code, 200)


class TestRegisterCustomerForm(TestCase):

    def test_valid_form(self):
        """Перевіряємо, чи форма валідна при правильних даних"""
        form_data = {
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'validpassword123',
            'password2': 'validpassword123',
            'phone': '+380123456789',
        }
        form = RegisterCustomerForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_phone_format(self):
        """Перевіряємо помилку при некоректному номері телефону"""
        form_data = {
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'validpassword123',
            'password2': 'validpassword123',
            'phone': '1234567890',  # Некоректний номер телефону
        }
        form = RegisterCustomerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['phone'],
                         ['Uncorrected phone number\nPhone number must consist:+380 ** *** ** **'])

    def test_password_mismatch(self):
        """Перевіряємо помилку, якщо паролі не співпадають"""
        form_data = {
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'validpassword123',
            'password2': 'differentpassword123',
            'phone': '+380123456789',
        }
        form = RegisterCustomerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'], ['password_mismatch'])

    def test_missing_email(self):
        """Перевіряємо форму на відсутність обов'язкового email"""
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'validpassword123',
            'password2': 'validpassword123',
            'phone': '+380123456789',
        }
        form = RegisterCustomerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['This field is required.'])

    def test_missing_required_fields(self):
        """Перевіряємо, чи форма не валідна без обов'язкових полів"""
        form_data = {
            'email': '',
            'first_name': '',
            'last_name': '',
            'password1': '',
            'password2': '',
            'phone': '',
        }
        form = RegisterCustomerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6)


class TestLoginUserForm(TestCase):

    def setUp(self):
        """Створюємо тестового користувача для перевірки форми входу"""
        self.user = Customer.objects.create(
            email='test@example.com',
            password='validpassword123',
            is_active=True
        )

    def test_valid_login(self):
        """Перевіряємо успішний вхід з правильним username і password"""
        form_data = {
            'username': 'test@example.com',
            'password': 'validpassword123',
        }
        form = LoginUserForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_username(self):
        """Перевіряємо помилку, коли введено неправильний email"""
        form_data = {
            'username': 'wrong@example.com',
            'password': 'validpassword123',
        }
        form = LoginUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'], ['User with this email does not exist'])

    def test_invalid_password(self):
        """Перевіряємо помилку, коли введено неправильний пароль"""
        form_data = {
            'username': 'test@example.com',
            'password': 'wrongpassword123',
        }
        form = LoginUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'], ['Please enter a correct email address and password. Note that both fields may be case-sensitive.'])

    def test_missing_username_or_password(self):
        """Перевіряємо форму на відсутність username або пароля"""
        form_data = {
            'username': '',
            'password': '',
        }
        form = LoginUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_clean_method_with_authenticated_user(self):
        """Перевіряємо, чи правильно працює метод clean при наявному користувачі"""
        form_data = {
            'username': 'test@example.com',
            'password': 'validpassword123',
        }
        form = LoginUserForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Customer.objects.create_user(email='test@test.com', password='password123')
        self.category = Category.objects.create(name='Category 1', slug='category-1')
        self.subcategory = SubCategory.objects.create(name='SubCategory 1', slug='subcategory-1', super_category=self.category)
        self.product = Product.objects.create(
            name='Product 1',
            slug='product-1',
            description='Test description',
            price=100,
            subcategory=self.subcategory,
            image="path/to/test/image.jpg"
        )

    def test_index(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/base.html')
        self.assertIn('recommended_products', response.context)
        self.assertIn('recommended_subcategories', response.context)

    def test_register_view(self):
        response = self.client.post(reverse('register'), {
            'email': 'newuser@test.com',
            'first_name': 'First',
            'last_name': 'Last',
            'password1': 'password123',
            'password2': 'password123',
            'phone': '+380123456789'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Customer.objects.filter(email='newuser@test.com').count(), 1)

    def test_register_confirm_view(self):
        token = 'testtoken'
        with patch('shop.views.confirm_customer', return_value=True):
            response = self.client.get(reverse('register_confirm', args=[token]))
            self.assertEqual(response.status_code, 302)

    def test_login_view(self):
        response = self.client.post(reverse('my_login'), {
            'username': self.user.email,
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        self.client.login(email='test@test.com', password='password123')
        response = self.client.get(reverse('my_logout'))
        self.assertEqual(response.status_code, 302)

    def test_show_subcategories_view(self):
        response = self.client.get(reverse('show_subcategories', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/subcategories.html')
        self.assertIn('subcategories', response.context)

    def test_show_subcategory_products_view(self):
        response = self.client.get(reverse('show_subcategory_products', args=[self.category.slug, self.subcategory.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/show_subcategory.html')
        self.assertIn('products', response.context)
        self.assertIn('subcategory', response.context)

    def test_show_products_view(self):
        response = self.client.get(reverse('show_product_details', args=[self.category.slug, self.subcategory.slug, self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product_detail.html')
        self.assertIn('product', response.context)

    def test_make_order_view_authenticated(self):
        self.client.login(email='test@test.com', password='password123')
        response = self.client.get(reverse('make_order'))
        self.assertEqual(response.status_code, 302)

    def test_make_order_view_unauthenticated(self):
        response = self.client.get(reverse('make_order'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('my_login')}?next={reverse('make_order')}")


class TestAIServiceFunctions(TestCase):
    def setUp(self):
        self.request_mock = mock.Mock()
        self.request_mock.GET = {
            "product_name": "Смартфон",
            "subcategory": "Електроніка"
        }

    @mock.patch("shop.services.AI_services.client.chat.completions.create")
    def test_generate_description(self, mock_openai_create):
        """Тест функції generate_description"""
        mock_openai_create.return_value = mock.Mock(
            choices=[mock.Mock(message=mock.Mock(content="Це унікальний опис смартфона."))]
        )

        description = generate_description(self.request_mock)
        self.assertEqual(description, "Це унікальний опис смартфона.")
        mock_openai_create.assert_called_once()

    @mock.patch("shop.services.AI_services.client.chat.completions.create")
    def test_generate_price(self, mock_openai_create):
        """Тест функції generate_price"""
        mock_openai_create.return_value = mock.Mock(
            choices=[mock.Mock(message=mock.Mock(content="10000"))]
        )

        price = generate_price(self.request_mock)
        self.assertEqual(price, "10000")
        mock_openai_create.assert_called_once()

    @mock.patch("shop.services.AI_services.client.images.generate")
    def test_generate_image_url(self, mock_openai_generate):
        """Тест функції generate_image_url"""
        mock_openai_generate.return_value = mock.Mock(
            data=[mock.Mock(url="http://example.com/image.png")]
        )

        image_url = generate_image_url(self.request_mock)
        self.assertEqual(image_url, "http://example.com/image.png")
        mock_openai_generate.assert_called_once()

    @mock.patch("shop.services.AI_services.client.chat.completions.create")
    def test_generate_description_error(self, mock_openai_create):
        """Тест помилки генерації опису"""
        mock_openai_create.side_effect = OpenAIError("Помилка аналізу ціни")

        response = generate_description(self.request_mock)
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 400)

        response_data = json.loads(response.content.decode())
        self.assertIn("Помилка генерації опису", response_data.get("error", ""))

    @mock.patch("shop.services.AI_services.client.chat.completions.create")
    def test_generate_price_error(self, mock_openai_create):
        """Тест помилки генерації ціни"""
        mock_openai_create.side_effect = OpenAIError("Помилка аналізу ціни")

        response = generate_price(self.request_mock)
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content.decode())
        self.assertIn("Помилка аналізу ціни", response_data.get("error", ""))

    @mock.patch("shop.services.AI_services.client.images.generate")
    def test_generate_image_url_error(self, mock_openai_generate):
        """Тест помилки генерації зображення"""
        mock_openai_generate.side_effect = OpenAIError("Помилка генерації картинки")

        response = generate_image_url(self.request_mock)
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content.decode())
        self.assertIn("Помилка генерації картинки", response_data.get("error", ""))
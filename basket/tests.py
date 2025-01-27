import json

from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Product, Category, SubCategory


class BasketViewsTestCase(TestCase):
    def setUp(self):
        """Створюємо тестові дані"""
        self.client = Client()
        category = Category.objects.create(name="Electronics", slug="electronics")
        subcategory = SubCategory.objects.create(name="Phones", slug="phones", super_category=category)
        self.product = Product.objects.create(
            id=1,
            name="iPhone 14",
            slug="iphone-14",
            description="New Apple iPhone",
            price=1000,
            subcategory=subcategory
        )
        self.basket_list_url = reverse('basket_list')
        self.add_basket_item_url = reverse('add_basket_item', args=[self.product.id])
        self.remove_basket_item_url = reverse('remove_basket_item', args=[self.product.id])
        self.clear_basket_url = reverse('clear_basket')
        self.update_product_quantity_url = reverse('update_quantity')

    def test_basket_list_view(self):
        """Перевірка відображення кошика"""
        response = self.client.get(self.basket_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')

    def test_add_basket_item(self):
        """Перевірка додавання товару в кошик"""
        session = self.client.session
        session['basket'] = []
        session.save()

        response = self.client.post(self.add_basket_item_url, {'url_from': self.basket_list_url})
        self.assertEqual(response.status_code, 302)  # Перенаправлення після додавання
        self.assertIn(str(self.product.id), self.client.session['basket'][0].values())

    def test_remove_basket_item(self):
        """Перевірка видалення товару з кошика"""
        session = self.client.session
        session['basket'] = [{'product_id': self.product.id}]
        session.save()

        response = self.client.post(self.remove_basket_item_url, {'url_from': self.basket_list_url})
        self.assertEqual(response.status_code, 302)  # Перенаправлення після видалення
        self.assertNotIn(self.product.id, self.client.session['basket'])

    def test_clear_basket(self):
        """Перевірка очищення кошика"""
        session = self.client.session
        session['basket'] = [self.product.id]
        session.save()

        response = self.client.get(self.clear_basket_url)
        self.assertEqual(response.status_code, 302)  # Перенаправлення після очищення
        self.assertNotIn('basket', self.client.session)

    def test_update_product_quantity(self):
        """Перевірка оновлення кількості товару"""
        session = self.client.session
        session['basket'] = [{'product_id': str(self.product.id), 'quantity': 1}]
        session.save()

        response = self.client.post(self.update_product_quantity_url,
                                    data=json.dumps({'product_id': self.product.id, 'new_quantity': 3}),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': True})

        # Перевіряємо, чи змінилась кількість товару в кошику
        basket = self.client.session['basket']
        updated_item = next((item for item in basket if item['product_id'] == str(self.product.id)), None)
        self.assertIsNotNone(updated_item)
        self.assertEqual(updated_item['quantity'], 3)

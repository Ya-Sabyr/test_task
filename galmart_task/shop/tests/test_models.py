from django.test import TestCase
from shop.models import Shop, Order

class ShopModelTest(TestCase):
    def test_create_shop(self):
        shop = Shop.objects.create(name="Test Shop", open=True)
        self.assertEqual(shop.name, "Test Shop")
        self.assertTrue(shop.open)

class OrderModelTest(TestCase):
    def test_create_order(self):
        shop = Shop.objects.create(name="Test Shop", open=True)
        order = Order.objects.create(status='Готовится', amount=100, shop=shop)
        self.assertEqual(order.status, 'Готовится')
        self.assertEqual(order.amount, 100)
        self.assertEqual(order.shop, shop)
from django.test import TestCase
from shop.models import Shop, Order
from shop.serializers import ShopSerializer, OrderSerializer

class ShopSerializerTest(TestCase):
    def test_shop_serialization(self):
        shop = Shop.objects.create(name="Test Shop", open=True)
        serializer = ShopSerializer(shop)
        data = serializer.data
        self.assertEqual(data['name'], "Test Shop")
        self.assertTrue(data['open'])

class OrderSerializerTest(TestCase):
    def test_order_serialization(self):
        shop = Shop.objects.create(name="Test Shop", open=True)
        order = Order.objects.create(status='Готовится', amount=100, shop=shop)
        serializer = OrderSerializer(order)
        data = serializer.data
        self.assertEqual(data['status'], 'Готовится')
        self.assertEqual(data['amount'], 100)
        self.assertEqual(data['shop'], shop.id)

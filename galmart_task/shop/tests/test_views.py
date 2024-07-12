from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from shop.models import Shop, Order

class ShopViewSetTest(APITestCase):
    def test_create_shop(self):
        url = reverse('shop-list')
        data = {'name': 'New Shop', 'open': True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Shop')
        self.assertTrue(response.data['open'])

class OrderViewSetTest(APITestCase):
    def setUp(self):
        self.shop = Shop.objects.create(name='Test Shop', open=True)

    def test_create_order(self):
        url = reverse('order-list')
        data = {'status': 'Готовится', 'amount': 100, 'shop': self.shop.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'Готовится')
        self.assertEqual(response.data['amount'], 100)
        self.assertEqual(response.data['shop'], self.shop.id)

    def test_update_order_status_completed(self):
        order = Order.objects.create(status='Готовится', amount=100, shop=self.shop)
        url = reverse('order-detail', args=[order.id])
        data = {'status': 'Завершен', 'amount': 100, 'shop': self.shop.id}
        with self.settings(API_ACCOUNTING_URL='http://127.0.0.1:8080/api/order', API_LOGIN_URL='http://127.0.0.1:8080/api/login'):
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['status'], 'Завершен')

class OrderViewSetTest(APITestCase):
    def setUp(self):
        self.shop = Shop.objects.create(name='Test Shop', open=True)

    def test_update_order_status_completed(self):
        order = Order.objects.create(status='Готовится', amount=100, shop=self.shop)
        url = reverse('order-detail', args=[order.id])
        data = {'status': 'Завершен', 'amount': 100, 'shop': self.shop.id}
        with self.settings(API_ACCOUNTING_URL='http://127.0.0.1:8080/api/order', API_LOGIN_URL='http://127.0.0.1:8080/api/login'):
            response = self.client.put(url, data, format='json')
            print(response.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['status'], 'Завершен')
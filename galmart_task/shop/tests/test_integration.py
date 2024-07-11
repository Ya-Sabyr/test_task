import responses
from django.test import TestCase
from rest_framework.test import APIClient
from shop.models import Shop, Order

class OrderIntegrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.shop = Shop.objects.create(name="Test Shop")
        self.order = Order.objects.create(
            shop=self.shop,
            status='Готовится',
            amount=90
        )

    @responses.activate
    def test_send_order_to_accounting(self):
        # Setup mock for login
        responses.add(
            responses.POST,
            'http://127.0.0.1:8000/test_api/login/',
            json={'token': 'fake_token'},
            status=200
        )

        # Setup mock for order
        responses.add(
            responses.POST,
            'http://127.0.0.1:8000/test_api/order/',
            json={'success': True},
            status=200
        )

        url = f'/api/v1/orders/{self.order.id}/'
        data = {'status': 'Завершен', 'amount': 90, 'shop': self.shop.id}

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)

        # Verify that the login was called once
        login_call = responses.calls[0].request
        self.assertEqual(login_call.url, 'http://127.0.0.1:8000/test_api/login/')
        self.assertEqual(login_call.method, 'POST')

        # Verify that the order API was called once
        order_call = responses.calls[1].request
        self.assertEqual(order_call.url, 'http://127.0.0.1:8000/test_api/order/')
        self.assertEqual(order_call.method, 'POST')

        # Verify the payload sent to the order API
        self.assertEqual(order_call.headers['Authorization'], 'Token fake_token')
        self.assertEqual(order_call.body.decode('utf-8'), '{"order_id": 1, "amount": 90, "shop_id": 1}')

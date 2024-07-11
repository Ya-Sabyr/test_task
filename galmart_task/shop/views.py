from rest_framework import viewsets
from .models import Shop, Order
from .serializers import ShopSerializer, OrderSerializer
import requests
from time import sleep
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        logging.debug(f"Order status updated to: {instance.status}")
        if instance.status == 'Завершен':
            self.send_order_to_accounting(instance)

    def send_order_to_accounting(self, order):
        login_url = "http://127.0.0.1:8000/test_api/login/"
        order_url = "http://127.0.0.1:8000/test_api/order/"
        payload = {'order_id': order.id, 'amount': order.amount, 'shop_id': order.shop.id}
        
        def authenticate():
            response = requests.post(login_url, data={'username': 'admin', 'password': 'admin'})
            if response.status_code == 200:
                logging.debug("Authentication successful.")
                return response.json().get('token')
            logging.debug("Authentication failed.")
            return None

        def send_data(token):
            headers = {'Authorization': f'Token {token}'}
            response = requests.post(order_url, headers=headers, json=payload)
            return response.status_code == 200

        token = authenticate()
        if not token:
            logging.debug("Authentication failed")  # Debugging output
            return

        attempts = 0
        max_attempts = 5
        while attempts < max_attempts:
            if send_data(token):
                logging.debug("Data sent successfully.")  # Debugging output
                break
            attempts += 1
            sleep(2 ** attempts)  # Exponential backoff
        else:
            logging.debug("Failed to send data after several attempts.")  # Debugging output

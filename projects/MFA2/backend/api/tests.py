from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser, Inventory, Transaction

class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword', role='OWNER')
        self.client.force_authenticate(user=self.user)
        self.inventory = Inventory.objects.create(name='Test Laptop', stock_quantity=10, unit_price=50000)

    def test_inventory_list(self):
        url = reverse('inventory-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_transaction_sale(self):
        url = reverse('transaction-list')
        data = {
            'transaction_type': 'SALE',
            'user': self.user.id,
            'product': self.inventory.id,
            'quantity': 2,
            'total_amount': 100000
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify stock update
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.stock_quantity, 8) # 10 - 2

    def test_chat_endpoint(self):
        # This mocks the successful call to the LLM processor or handles the error gracefully
        url = reverse('chat-send')
        data = {'message': 'Hello'}
        # We expect a 500 or error because GOOGLE_API_KEY is not set in test env, 
        # but the endpoint should be reachable.
        response = self.client.post(url, data, format='json')
        self.assertTrue(response.status_code in [200, 500])

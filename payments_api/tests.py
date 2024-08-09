from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from django.contrib.auth.models import User

from payments_api.models import Balance, Transaction


class PaymentsAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='Testpassword123')
        self.client.login(username='testuser', password='Testpassword123')

        self.balance = Balance.objects.create(user=self.user, amount=100.00)

    def test_balance_creation(self):
        self.assertEqual(self.balance.user, self.user)
        self.assertEqual(self.balance.amount, 100.00)

    def test_transaction_creation(self):
        receiver = User.objects.create_user(username='receiver', password='Receiverpassword123')
        transaction = Transaction.objects.create(sender=self.user, receiver=receiver, amount=50.00)

        self.assertEqual(transaction.sender, self.user)
        self.assertEqual(transaction.receiver, receiver)
        self.assertEqual(transaction.amount, 50.00)

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_view_post_valid(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'Testpassword123'
        })
        self.assertRedirects(response, reverse('start_page'))

    def test_login_view_post_invalid(self):
        response = self.client.post(reverse('login'), {
            'username': 'invaliduser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_balance_api_view(self):
        response = self.client.get(reverse('payments_api:balance'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance_rub'], 1.00)

    def test_deposit_api_view(self):
        data = {'amount': 50.00}
        response = self.client.post(reverse('payments_api:deposit'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['new_balance'], 150.00)

    def test_deposit_api_view_invalid_amount(self):
        data = {'amount': -50.00}
        response = self.client.post(reverse('payments_api:deposit'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_transfer_api_view(self):
        receiver = User.objects.create_user(username='receiver', password='Receiverpassword123')
        Balance.objects.create(user=receiver, amount=0.00)

        data = {"amount": 50.0, "receiver_id": 2}
        response = self.client.post(reverse('payments_api:transfer'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['new_sender_balance'], 50.00)
        self.assertEqual(response.data['new_receiver_balance'], 50.00)

    def test_transfer_api_view_insufficient_funds(self):
        receiver = User.objects.create_user(username='receiver', password='receiverpassword')
        Balance.objects.create(user=receiver, amount=0.00)

        data = {"amount": 200.00, "receiver_id": 2}
        response = self.client.post(reverse('payments_api:transfer'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Недостаточно средств')

    def test_transfer_api_view_invalid_amount(self):
        receiver = User.objects.create_user(username='receiver', password='receiverpassword')
        Balance.objects.create(user=receiver, amount=0.00)

        data = {"amount": -50.00, "receiver_id": 2}
        response = self.client.post(reverse('payments_api:transfer'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

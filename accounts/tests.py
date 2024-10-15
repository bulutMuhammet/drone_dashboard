from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User


class AccountsAPITestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser@testuser.com', email="testuser@testuser.com",
                                             password='testpass123')

    def test_register(self):
        url = reverse('register-api')
        data = {
            'username': 'newuser@example.com',
            'password': 'newpass123',
            'email': 'newuser@example.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        url = reverse('login-api')
        data = {
            'email': 'testuser@testuser.com',
            'password': 'testpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

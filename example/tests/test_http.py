# example/tests/test_http.py
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase


class AuthenticationTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_can_sign_up(self):
        password = 'pAssw0rd!'
        # NOTE: fields password1, password2 used in tutorial
        response = self.client.post(reverse('sign_up'), data={
            'username': 'user@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': password,
            'password_confirm': password,
        })
        user = get_user_model().objects.last()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response.data['id'], user.id)
        self.assertEqual(response.data['username'], user.username)
        self.assertEqual(response.data['first_name'], user.first_name)
        self.assertEqual(response.data['last_name'], user.last_name)

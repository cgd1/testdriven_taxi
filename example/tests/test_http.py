# example/tests/test_http.py
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from example.serializers import TripSerializer, UserSerializer
from example.models import Trip

"""
To run these tests: python manage.py test example.tests
"""

PASSWORD = 'pAssw0rd!'


def create_user(username='user@example.com', password=PASSWORD): # new
    return get_user_model().objects.create_user(
        username=username, password=password)


class AuthenticationTest(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.login(username=self.user.username, password=PASSWORD)

    def test_user_can_sign_up(self):
        response = self.client.post(reverse('sign_up'), data={
            'username': 'user2@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': PASSWORD,
            'password2': PASSWORD,
        })
        user = get_user_model().objects.last()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response.data['id'], user.id)
        self.assertEqual(response.data['username'], user.username)
        self.assertEqual(response.data['first_name'], user.first_name)
        self.assertEqual(response.data['last_name'], user.last_name)

    def test_sign_up_wrong_confirmation_password(self):
        response = self.client.post(reverse('sign_up'), data={
            'username': 'user@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': PASSWORD,
            'password2': 'password2',
        })
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_user_can_log_in(self):
        response = self.client.post(reverse('log_in'), data={
            'username': self.user.username,
            'password': PASSWORD,
        })
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data['username'], self.user.username)

    def test_login_wrong_password(self):
        response = self.client.post(reverse('log_in'), data={
            'username': self.user.username,
            'password': 'password',
        })
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_user_can_log_out(self):
        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.post(reverse('log_out'))
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)


class HttpTripTest(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.login(username=self.user.username, password=PASSWORD)

    def test_user_can_list_trips(self):
        trips = [
            Trip.objects.create(pick_up_address='A', drop_off_address='B'),
            Trip.objects.create(pick_up_address='B', drop_off_address='C')
        ]
        response = self.client.get(reverse('trip:trip_list'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        exp_trip_nks = [trip.nk for trip in trips]
        act_trip_nks = [trip.get('nk') for trip in response.data]
        self.assertCountEqual(exp_trip_nks, act_trip_nks)

    def test_user_can_retrieve_trip_by_nk(self):
        trip = Trip.objects.create(pick_up_address='A', drop_off_address='B')
        response = self.client.get(trip.get_absolute_url())
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # data is a DRF.ReturnList object of length 1 containing the data-dictionary
        self.assertEqual(trip.nk, response.data[0].get('nk'))


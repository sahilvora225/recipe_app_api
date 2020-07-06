from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicUserApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        payload = {'email': 'sahilya@sahil.com', 'password': 'sahil1234'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEquals(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        payload = {'email': 'sahil@sahil.com', 'password': 'sahil123'}
        user = create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        payload = {'email': 'sahil@sahil.com', 'password': 'sa'}
        res = self.client.post(CREATE_USER_URL, payload)

        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_create_user_token_success(self):
        payload = {'email': 'sahil@sahil.com', 'password': 'sahil123'}
        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_token_invalid_credentials(self):
        create_user(email='sahil@sahil.com', password='sahil123')
        payload = {'email': 'sahil@sahil.com', 'password': 'sahilsahil'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_token_user_not_exist(self):
        payload = {'email': 'sahil@sahil.com', 'password': 'sahil123'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_token_missing_parameter(self):
        create_user(email='sahil@sahil.com', password='sahil123')
        payload = {'email': 'sahil@sahil.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

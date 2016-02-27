from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AccountTests(APITestCase):
    TEST_LOGIN = 'test@test.ru'
    TEST_PASSWORD = 'test12345'

    def test_1_create_account(self):
        url = reverse('register')
        data = {'email': self.TEST_LOGIN, 'password': self.TEST_PASSWORD}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, self.TEST_LOGIN)


    def test_2_get_token(self):
        user = User.objects.create_user(username=self.TEST_LOGIN, email=self.TEST_LOGIN, password=self.TEST_PASSWORD)
        url = reverse('get-token')
        data = {'email': self.TEST_LOGIN, 'password': self.TEST_PASSWORD}
        response = self.client.post(url, data, format='json')
        self.assertIn('token', response.data)


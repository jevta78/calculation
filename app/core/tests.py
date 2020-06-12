from .models import InputNumbers, Sums
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

def sample_user(email='test@test.com', password='testpass'):
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_inputnumbers_str(self):
        inputnum = InputNumbers.objects.create(
            user=sample_user(),
            list_num = 22
        )
        self.assertEqual(str(inputnum), str(inputnum.list_num))


ADD_URL = reverse('core:add_num')
CALCULATE_URL = reverse('core:calculate')


def sample_inputNumbers(user, list_num, **params):
    return InputNumbers.objects.create(user=user, list_num=list_num)


class PublicInputNumApiTest(TestCase):
    '''Test unauthenticated API access'''

    def setUp(self):
        self.client = APIClient()

    def test_required_auth(self):
        res = self.client.get(ADD_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class InputNumCreateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_num(self):

        payload = {
            'user': self.user,
            'list_num': 25
        }

        res = self.client.post(ADD_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        num = InputNumbers.objects.filter().first()
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(num, key))


class CalculationTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'password'
        )
        payload = {
            'user': self.user,
            'list_num': 22
        }
        payload2 = {
            'user': self.user,
            'list_num': 28
        }
        # num1 = sample_inputNumbers(user=self.user, list_num = 22)
        self.num1 = self.client.post(ADD_URL, payload)
        # self.num2 = sample_inputNumbers(user=self.user, list_num=28)
        self.num1 = self.client.post(ADD_URL, payload2)

        self.client.force_authenticate(self.user)

    def test_calculation(self):
        payload = {
            'user': self.user,
            'list_num': 22
        }
        payload2 = {
            'user': self.user,
            'list_num': 28
        }
        # num1 = sample_inputNumbers(user=self.user, list_num = 22)
        self.num1 = self.client.post(ADD_URL, payload)
        # self.num2 = sample_inputNumbers(user=self.user, list_num=28)
        self.num2 = self.client.post(ADD_URL, payload2)

        res = self.client.get(CALCULATE_URL, self.num1, self.num2)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        suma = Sums.objects.filter().first()
        self.assertEqual(suma.calcSum, 50)
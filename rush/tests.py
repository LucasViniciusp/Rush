from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from model_bakery import baker
from parameterized import parameterized

from rush.models import User


# Create your tests here.
class BaseTest(TestCase):
    def setUp(self):
        """
        Setup API client with authentication
        """
        self.client = APIClient()
        self.user = baker.make(User, username='setupuser')


class RegisterViewTestCase(BaseTest):
    @parameterized.expand([
        'GET', 'PUT', 'PATCH', 'DELETE'
    ])
    def test_register_not_allowed_methods(self, method):
        response = self.client.generic(
            method=method,
            path=f'/api/register/'
        )
        self.assertEqual(
            response.status_code, 
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_register_user(self):
        """
        Should be possible to register a user
        """
        new_user_data = {
            'username': 'test',
            'password': 'test',
            'email': 'test@test.com',
            'first_name': 'test',
	        'last_name': 'test'
        }
        response = self.client.post(
            path=f'/api/register/',
            data=new_user_data
        )
        new_user = User.objects.last()

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(new_user_data['password'], new_user.password)   #Assert password has been encrypted

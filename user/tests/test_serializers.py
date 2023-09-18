from rest_framework.test import APITestCase

from user.models import User
from user.serializers import UserSerializer


class UserSerializerTestCase(APITestCase):
    def test_user_serializer_valid_data(self):
        data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

    def test_user_serializer_password_mismatch(self):
        data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword',
            'confirm_password': 'mismatchpassword'
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['non_field_errors'][0], "Password and Confirm_Password doesn't match.")

    def test_user_serializer_duplicate_username(self):
        User.objects.create_user(username='existinguser', password='testpassword', first_name='Test', last_name='User')

        data = {
            'username': 'existinguser',
            'name': 'Test User',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }

        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['username'][0], 'user with this username already exists.')

    def test_user_serializer_create(self):
        data = {
            'username': 'test',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }

        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        user = serializer.create(serializer.validated_data)
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')

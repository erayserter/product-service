from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from user.models import User


class CreateViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_view_success(self):
        url = reverse('user-create')

        data = {
            'username': 'test',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('username'), 'test')
        self.assertEqual(response.data.get('first_name'), 'Test')
        self.assertEqual(response.data.get('last_name'), 'User')

    def test_create_view_duplicate_username(self):
        User.objects.create_user(username='test', password='testpassword', first_name="Test", last_name="User")

        url = reverse('user-create')

        data = {
            'username': 'test',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(username='test', password='testpassword', first_name='Test', last_name='User')
        self.user.save()

    def test_login_view_success(self):
        url = reverse('token_obtain_pair')

        data = {
            'username': 'test',
            'password': 'testpassword'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsNotNone(response.data.get('access'))
        self.assertIsNotNone(response.data.get('refresh'))

    def test_login_view_invalid_credentials(self):
        url = reverse('token_obtain_pair')

        data = {
            'username': 'test',
            'password': 'wrongpassword'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail'), 'No active account found with the given credentials')

    def test_login_refresh_view(self):
        url = reverse('token_obtain_pair')

        data = {
            'username': 'test',
            'password': 'testpassword'
        }

        response = self.client.post(url, data, format='json')

        url = reverse('token_refresh')

        data = {
            'refresh': response.data.get('refresh')
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('access'))


class UserDetailViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='testpassword', first_name='Test', last_name='User')
        self.client.force_authenticate(user=self.user)

    def test_get_user_detail(self):
        url = reverse('user-detail', kwargs={
            "username": self.user.username
        })

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'test')
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'User')

    def test_get_user_detail_without_auth(self):
        self.client.logout()

        url = reverse('user-detail', kwargs={
            "username": self.user.username
        })

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_another_user_detail(self):
        user2 = User.objects.create_user(username='test2', password='testpassword2', first_name='Test2',
                                         last_name='User2')

        url = reverse('user-detail', kwargs={
            "username": user2.username
        })

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user_success(self):
        url = reverse('user-detail', kwargs={
            "username": self.user.username
        })

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_another_user(self):
        user2 = User.objects.create_user(username='test2', password='testpassword2', first_name='Test2', last_name='User2')

        url = reverse('user-detail', kwargs={
            "username": user2.username
        })

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

from django.urls import reverse

from rest_framework.test import APITestCase, APIClient

from user.models import User


class BaseProductAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='test',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )
        self.client.force_authenticate(user=self.user)
        self.data = {
            "name": "Macbook Air M1 (2020)",
            "description": "M1 Chip Mac",
            "brand": "Apple",
            "price_unit": "TRY",
            "price": 17500,
            "stock": 8
        }

    def client_create_product(self):
        url = reverse('products')

        return self.client.post(url, self.data, format='json')

    def client_retrieve_product(self, code):
        url = reverse('product-detail', kwargs={
            "code": code
        })

        return self.client.get(url)

    def client_update_product(self, code, data):
        url = reverse('product-detail', kwargs={
            "code": code
        })

        return self.client.patch(url, data, format='json')

    def client_delete_product(self, code):
        url = reverse('product-detail', kwargs={
            'code': code
        })

        return self.client.delete(url)

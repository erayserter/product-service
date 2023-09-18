from django.urls import reverse

from rest_framework import status

from product.models import Product
from product.tests.test_views import BaseProductAPITestCase


class ListViewTestCase(BaseProductAPITestCase):
    def test_list_view(self):
        product = Product.objects.create(**self.data)

        url = reverse('products')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0].get('code'), str(product.code))

    def test_list_view_without_auth(self):
        self.client.logout()

        url = reverse('products')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filtered_name_list_view(self):
        url = reverse('products')

        self.client.post(url, self.data, format='json')
        self.data['name'] = 'Test'
        self.client.post(url, self.data, format='json')

        url = reverse('products') + '?name=Tes'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test')

    def test_filtered_code_list_view(self):
        url = reverse('products')

        create_response = self.client.post(url, self.data, format='json')
        self.client.post(url, self.data, format='json')

        url = reverse('products') + f'?code={create_response.data["code"]}'

        list_response = self.client.get(url)

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)
        self.assertEqual(list_response.data[0]['code'], create_response.data["code"])

    def test_filtered_brand_list_view(self):
        url = reverse('products')

        self.client.post(url, self.data, format='json')
        self.data['brand'] = 'testbrand'
        self.client.post(url, self.data, format='json')

        url = reverse('products') + '?brand=test'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['brand'], 'testbrand')

    def test_filtered_price_list_view(self):
        url = reverse('products')

        self.client.post(url, self.data, format='json')
        self.data['price'] = 25000
        self.client.post(url, self.data, format='json')

        url = reverse('products') + '?price_interval=20000-25500'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(float(response.data[0]['price']), 25000)

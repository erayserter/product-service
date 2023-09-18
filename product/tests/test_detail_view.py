from django.urls import reverse

from rest_framework import status

from product.models import Product
from product.tests.test_views import BaseProductAPITestCase


class DetailViewTestCase(BaseProductAPITestCase):
    def test_retrieve_view_found(self):
        url = reverse('products')

        response = self.client.post(url, self.data, format='json')

        product = Product.objects.get(code=response.data['code'])

        url = reverse('product-detail', kwargs={
            "code": product.code
        })

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), product.name)
        self.assertEqual(response.data.get('description'), product.description)
        self.assertEqual(response.data.get('brand'), product.brand)
        self.assertEqual(float(response.data.get('price')), product.price)
        self.assertEqual(response.data.get('price_unit'), product.price_unit)
        self.assertEqual(response.data.get('stock'), product.stock)
        self.assertTrue(response.data.get('has_stock'))
        self.assertEqual(response.data.get('code'), str(product.code))
        self.assertEqual(response.data.get('owner'), self.user.username)

    def test_retrieve_view_not_found(self):
        url = reverse('product-detail', kwargs={
            "code": '123'
        })

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_view(self):
        url = reverse('products')

        response = self.client.post(url, self.data, format='json')

        url = reverse('product-detail', kwargs={
            "code": response.data['code']
        })

        data = {
            "name": "Test Product"
        }

        response = self.client.patch(url, data, format='json')

        product = Product.objects.get(code=response.data['code'])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), data['name'])
        self.assertEqual(product.name, data['name'])

    def test_delete_view(self):
        url = reverse('products')

        response = self.client.post(url, self.data, format='json')

        self.assertTrue(Product.objects.exists())

        url = reverse('product-detail', kwargs={
            'code': response.data['code']
        })

        self.client.delete(url)

        self.assertFalse(Product.objects.exists())
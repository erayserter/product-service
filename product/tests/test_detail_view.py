from django.urls import reverse

from rest_framework import status

from product.models import Product
from product.tests.test_views import BaseProductAPITestCase


class DetailViewTestCase(BaseProductAPITestCase):
    def test_retrieve_found(self):
        response = self.client_create_product()

        product = Product.objects.get(code=response.data['code'])

        response = self.client_retrieve_product(product.code)

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

    def test_retrieve_not_found(self):
        response = self.client_retrieve_product("123")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update(self):
        data = {"name": "Test Product"}

        response_create = self.client_create_product()
        response_update = self.client_update_product(response_create.data['code'], data)

        product = Product.objects.get(code=response_update.data['code'])

        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(response_update.data.get('name'), data['name'])
        self.assertEqual(product.name, data['name'])

    def test_delete(self):
        response_create = self.client_create_product()

        self.assertTrue(Product.objects.exists())

        response_delete = self.client_delete_product(response_create.data['code'])

        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.exists())

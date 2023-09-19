from rest_framework import status

from product.tests.test_views import BaseProductAPITestCase


class CreateViewTestCase(BaseProductAPITestCase):
    def test_view_success(self):
        response = self.client_create_product()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('name'), self.data['name'])
        self.assertEqual(response.data.get('description'), self.data['description'])
        self.assertEqual(response.data.get('brand'),self. data['brand'])
        self.assertEqual(float(response.data.get('price')), self.data['price'])
        self.assertEqual(response.data.get('price_unit'), self.data['price_unit'])
        self.assertEqual(response.data.get('stock'), self.data['stock'])
        self.assertTrue(response.data.get('has_stock'))
        self.assertIsNotNone(response.data.get('code'))
        self.assertEqual(response.data.get('owner'), self.user.username)

    def test_success_with_code(self):
        self.data['code'] = self.data.get('name').replace(' ', '-')
        response = self.client_create_product()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('code'), self.data['code'])

    def test_duplicate_code(self):
        self.data['code'] = self.data.get('name').replace(' ', '-')
        response_first = self.client_create_product()
        response_second = self.client_create_product()

        self.assertEqual(response_first.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_first.data.get('code'), self.data['code'])
        self.assertEqual(response_second.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_currency(self):
        self.data['price_unit'] = 'TL'
        response = self.client_create_product()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_without_auth(self):
        self.client.logout()

        response = self.client_create_product()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

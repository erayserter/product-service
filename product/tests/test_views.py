from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from user.models import User

from product.models import Product


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
            "price_unit": "TL",
            "price": 17500,
            "stock": 8
        }


class CreateViewTestCase(BaseProductAPITestCase):
    def test_create_view_success(self):
        url = reverse('products')

        response = self.client.post(url, self.data, format='json')

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

    def test_create_view_success_with_code(self):
        url = reverse('products')

        self.data['code'] = self.data.get('name').replace(' ', '-')

        response = self.client.post(url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('code'), self.data['code'])

    def test_create_view_duplicate_code(self):
        url = reverse('products')

        self.data['code'] = self.data.get('name').replace(' ', '-')

        response_first = self.client.post(url, self.data, format='json')
        response_second = self.client.post(url, self.data, format='json')

        self.assertEqual(response_first.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_first.data.get('code'), self.data['code'])
        self.assertEqual(response_second.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_view_without_auth(self):
        self.client.logout()

        url = reverse('products')

        response = self.client.post(url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


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

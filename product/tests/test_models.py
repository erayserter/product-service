from django.test import TestCase

from product.models import Product
from user.models import User


class ProductModelTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='test',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )

    def test_create_product(self):
        data = {
            "name": "Macbook Air M1 (2020)",
            "description": "M1 Chip Mac",
            "brand": "Apple",
            "owner": self.user,
            "price_unit": "TRY",
            "price": 17500,
            "stock": 8
        }
        product = Product.objects.create(**data)

        self.assertEqual(product.name, data['name'])
        self.assertEqual(product.description, data['description'])
        self.assertEqual(product.brand, data['brand'])
        self.assertEqual(product.price_unit, data['price_unit'])
        self.assertEqual(product.price, data['price'])
        self.assertEqual(product.stock, data['stock'])
        self.assertIsNotNone(product.code)
        self.assertEqual(self.user, product.owner)
        self.assertTrue(product.has_stock)


class ProductMethodTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='test',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )

    def test_has_stock(self):
        data = {
            "name": "Macbook Air M1 (2020)",
            "description": "M1 Chip Mac",
            "brand": "Apple",
            "owner": self.user,
            "price_unit": "TRY",
            "price": 17500,
            "stock": 8
        }
        product = Product.objects.create(**data)

        self.assertTrue(product.has_stock)

    def test_zero_stock(self):
        data = {
            "name": "Macbook Air M1 (2020)",
            "description": "M1 Chip Mac",
            "brand": "Apple",
            "owner": self.user,
            "price_unit": "TRY",
            "price": 17500,
            "stock": 0
        }
        product = Product.objects.create(**data)

        self.assertFalse(product.has_stock)

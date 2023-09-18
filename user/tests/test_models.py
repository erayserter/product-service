from django.test import TestCase

from user.models import User


class UserModelTest(TestCase):
    def test_create_user(self):
        username = "testuser"
        first_name = "Test"
        last_name = "User"
        password = "testpassword"

        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)

        self.assertEqual(user.username, username)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.check_password(password))

    def test_create_superuser(self):
        username = "adminuser"
        first_name = "Admin"
        last_name = "User"
        password = "adminpassword"

        superuser = User.objects.create_superuser(username=username, first_name=first_name, last_name=last_name, password=password)

        self.assertEqual(superuser.username, username)
        self.assertEqual(superuser.first_name, first_name)
        self.assertEqual(superuser.last_name, last_name)
        self.assertTrue(superuser.is_admin)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.check_password(password))


class UserMethodTest(TestCase):
    def test_get_full_name(self):
        user = User(username="testuser", first_name="Test", last_name="User")
        self.assertEqual(user.get_full_name(), "Test User")

    def test_is_staff(self):
        user = User(username="testuser", first_name="Test", last_name="User")
        self.assertFalse(user.is_staff)

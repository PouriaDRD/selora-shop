from django.test import TestCase
from rest_framework.exceptions import ValidationError

from accounts.services import UserService


class UserServiceTests(TestCase):

    def test_create_user(self):
        user = UserService.create_user(
            username="Pouria",
            password="12345678",
        )

        self.assertEqual(user.username, "pouria")

    def test_duplicate_username(self):
        UserService.create_user(
            username="pouria",
            password="12345678",
        )

        with self.assertRaises(ValidationError):
            UserService.create_user(
                username="pouria",
                password="12345678",
            )

    def test_empty_username(self):
        with self.assertRaises(ValidationError):
            UserService.create_user(
                username="",
                password="12345678",
            )

    def test_update_last_login(self):
        user = UserService.create_user(
            username="pouria",
            password="12345678",
        )

        self.assertIsNone(user.last_login)

        UserService.update_last_login(user)

        user.refresh_from_db()

        self.assertIsNotNone(user.last_login)

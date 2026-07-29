from django.test import TestCase

from accounts.repositories import UserRepository
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRepositoryTests(TestCase):

    def test_create(self):
        user = UserRepository.create(
            username="pouria",
            password="12345678",
        )
        self.assertEqual(user.username, "pouria")

    def test_exists(self):
        User.objects.create_user(
            username="pouria",
            password="12345678",
        )

        self.assertTrue(UserRepository.exists(username="pouria"))

    def test_get_by_username(self):
        created = User.objects.create_user(
            username="pouria",
            password="12345678",
        )

        found = UserRepository.get_by_username("pouria")

        self.assertEqual(found.id, created.id)  # type: ignore

    def test_delete(self):
        user = User.objects.create_user(
            username="pouria",
            password="12345678",
        )

        UserRepository.delete(user)

        self.assertFalse(User.objects.filter(username="pouria").exists())

    def test_bulk_create(self):
        users = UserRepository.bulk_create(
            [
                {
                    "username": "pouria",
                    "password": "12345678",
                },
                {
                    "username": "pouria2",
                    "password": "12345678",
                },
            ]
        )

        self.assertEqual(len(users), 2)

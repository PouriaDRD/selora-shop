from django.test import TestCase

from accounts.enums import UserRole, UserStatus
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTests(TestCase):

    def test_full_name(self):
        user = User.objects.create_user(
            username="pouria",
            password="12345678",
            first_name="Pouria",
            last_name="Darandi",
        )

        self.assertEqual(user.full_name, "Pouria Darandi")  # type: ignore

    def test_full_name_fallback(self):
        user = User.objects.create_user(
            username="pouria",
            password="12345678",
        )

        self.assertEqual(user.full_name, "pouria")  # type: ignore

    def test_is_staff_admin(self):
        user = User.objects.create_superuser(
            username="admin",
            password="12345678",
        )  # type: ignore

        self.assertTrue(user.is_staff)

    def test_is_superuser_admin(self):
        user = User.objects.create_superuser(
            username="admin",
            password="12345678",
        )  # type: ignore

        self.assertTrue(user.is_superuser)

    def test_role_superuser(self):
        user = User.objects.create_superuser(
            username="admin",
            password="12345678",
        )  # type: ignore

        self.assertEqual(user.role, UserRole.SUPERUSER)

    def test_role_user(self):
        user = User.objects.create_user(
            username="user",
            password="12345678",
        )  # type: ignore

        self.assertEqual(user.role, UserRole.USER)  # type: ignore

    def test_status_active(self):
        user = User.objects.create_user(
            username="user",
            password="12345678",
        )  # type: ignore

        self.assertEqual(user.status, UserStatus.ACTIVE)  # type: ignore

    def test_is_superuser_normal_user(self):
        user = User.objects.create_user(
            username="user",
            password="12345678",
        )

        self.assertFalse(user.is_superuser)

    def test_is_staff_normal_user(self):
        user = User.objects.create_user(
            username="user",
            password="12345678",
        )

        self.assertFalse(user.is_staff)

    def test_is_active(self):
        user = User.objects.create_user(
            username="user",
            password="12345678",
        )

        self.assertTrue(user.is_active)

    def test_str(self):
        user = User.objects.create_user(
            username="pouria",
            password="12345678",
        )

        self.assertEqual(str(user), "pouria")

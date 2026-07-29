from django.test import TestCase

from django.contrib.auth import get_user_model

from accounts.api.v1.serializers import UserSerializer

User = get_user_model()


class UserSerializerTests(TestCase):

    def test_serializer_fields(self):
        user = User.objects.create_user(
            username="pouria",
            password="12345678",
        )

        data = UserSerializer(user).data

        self.assertIn("id", data)
        self.assertIn("username", data)
        self.assertIn("full_name", data)
        self.assertIn("role", data)
        self.assertIn("status", data)

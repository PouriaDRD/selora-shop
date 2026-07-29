from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfileAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="pouria",
            password="12345678",
        )

    def test_authenticated_user_profile(self):
        self.client.force_authenticate(self.user)  # type: ignore

        response = self.client.get(reverse("profile"))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_unauthenticated_user(self):
        response = self.client.get(reverse("profile"))

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

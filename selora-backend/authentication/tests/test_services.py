from django.test import RequestFactory, TestCase
from rest_framework.exceptions import ValidationError

from accounts.services import UserService
from authentication.models import LoginHistoryModel
from authentication.services.auth import AuthService
from authentication.services.login_history import LoginHistoryService


class AuthServiceTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def _build_request(self):
        request = self.factory.post("/auth/login", data={})
        request.META.update(
            {
                "REMOTE_ADDR": "127.0.0.1",
                "HTTP_USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            }
        )
        return request

    def test_register_creates_user_and_returns_auth_payload(self):
        request = self._build_request()

        response = AuthService.register(
            username="TestUser",
            password="StrongPass123",
            request=request,  # type: ignore
        )

        self.assertIn("access", response)
        self.assertIn("refresh", response)
        self.assertEqual(response["user"], "testuser")
        self.assertTrue(
            LoginHistoryModel.objects.filter(
                user__username="testuser", is_successful=True
            ).exists()
        )

    def test_login_authenticates_existing_user_and_records_history(self):
        user = UserService.create_user(username="TestUser", password="StrongPass123")
        request = self._build_request()

        response = AuthService.login(
            username="TestUser",
            password="StrongPass123",
            request=request,  # type: ignore
        )

        self.assertIn("access", response)
        self.assertEqual(response["user"], "testuser")
        self.assertTrue(
            LoginHistoryModel.objects.filter(user=user, is_successful=True).exists()
        )

    def test_login_invalid_credentials_records_failed_history(self):
        user = UserService.create_user(username="TestUser", password="StrongPass123")
        request = self._build_request()

        with self.assertRaises(ValidationError):
            AuthService.login(
                username="TestUser",
                password="WrongPassword123",
                request=request,  # type: ignore
            )

        history = (
            LoginHistoryModel.objects.filter(user=user, is_successful=False)
            .order_by("-created_at")
            .first()
        )
        self.assertIsNotNone(history)
        self.assertEqual(history.failure_reason, "نام کاربری یا رمز عبور اشتباه است.")  # type: ignore

    def test_login_history_service_creates_success_and_failure_records(self):
        user = UserService.create_user(username="TestUser", password="StrongPass123")
        request = self._build_request()

        LoginHistoryService.create_success(user, request)  # type: ignore
        success_history = LoginHistoryModel.objects.filter(
            user=user, is_successful=True
        ).first()
        self.assertIsNotNone(success_history)

        failed_history = LoginHistoryService.create_failed(
            username="testuser",
            request=request,  # type: ignore
            reason="Invalid credentials",
        )

        self.assertIsNotNone(failed_history)
        self.assertFalse(failed_history.is_successful)  # type: ignore
        self.assertEqual(failed_history.failure_reason, "Invalid credentials")  # type: ignore

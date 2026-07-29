from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from accounts.validators.user import username_validator


class UsernameValidatorTests(SimpleTestCase):

    def test_valid_username(self):
        username_validator("pouria_123")

    def test_valid_username_with_dash(self):
        username_validator("pouria-123")

    def test_invalid_username(self):
        with self.assertRaises(ValidationError):
            username_validator("پوریا")

    def test_invalid_special_characters(self):
        with self.assertRaises(ValidationError):
            username_validator("test@test")

    def test_invalid_username_with_space(self):
        with self.assertRaises(ValidationError):
            username_validator("test test")

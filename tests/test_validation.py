"""Tests unitaires - Validation"""

from app.services.validation import validate_email, validate_password


class TestValidateEmail:
    def test_valid_emails(self):
        assert validate_email("user@example.com")
        assert validate_email("user.name@example.co.uk")
        assert validate_email("user+tag@example.org")

    def test_invalid_emails(self):
        assert not validate_email("")
        assert not validate_email("user")
        assert not validate_email("user@")
        assert not validate_email("@example.com")
        assert not validate_email("user@.com")


class TestValidatePassword:
    def test_valid_passwords(self):
        assert validate_password("Password1")
        assert validate_password("MyPass123")
        assert validate_password("ABCdef123")

    def test_invalid_passwords(self):
        assert not validate_password("")
        assert not validate_password("short1A")
        assert not validate_password("nouppercase1")
        assert not validate_password("NOLOWERCASE1")
        assert not validate_password("NoDigits!")

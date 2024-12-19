# test_security.py
from builtins import RuntimeError, ValueError, isinstance, str
import pytest
import secrets
import bcrypt
from app.utils.security import hash_password, verify_password, generate_verification_token

def test_hash_password():
    """Test that hashing password returns a bcrypt hashed string."""
    password = "secure_password"
    hashed = hash_password(password)
    assert hashed is not None
    assert isinstance(hashed, str)
    assert hashed.startswith('$2b$')

def test_hash_password_with_different_rounds():
    """Test hashing with different cost factors."""
    password = "secure_password"
    rounds = 10
    hashed_10 = hash_password(password, rounds)
    rounds = 12
    hashed_12 = hash_password(password, rounds)
    assert hashed_10 != hashed_12, "Hashes should differ with different cost factors"

def test_verify_password_correct():
    """Test verifying the correct password."""
    password = "secure_password"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True

def test_verify_password_incorrect():
    """Test verifying the incorrect password."""
    password = "secure_password"
    hashed = hash_password(password)
    wrong_password = "incorrect_password"
    assert verify_password(wrong_password, hashed) is False

def test_verify_password_invalid_hash():
    """Test verifying a password against an invalid hash format."""
    with pytest.raises(ValueError):
        verify_password("secure_password", "invalid_hash_format")

@pytest.mark.parametrize("password", [
    "",
    " ",
    "a"*100  # Long password
])
def test_hash_password_edge_cases(password):
    """Test hashing various edge cases."""
    hashed = hash_password(password)
    assert isinstance(hashed, str) and hashed.startswith('$2b$'), "Should handle edge cases properly"

def test_verify_password_edge_cases():
    """Test verifying passwords with edge cases."""
    password = " "
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True
    assert verify_password("not empty", hashed) is False

# This function tests the error handling when an internal error occurs in bcrypt
def test_hash_password_internal_error(monkeypatch):
    """Test proper error handling when an internal bcrypt error occurs."""
    def mock_bcrypt_gensalt(rounds):
        raise RuntimeError("Simulated internal error")

    monkeypatch.setattr("bcrypt.gensalt", mock_bcrypt_gensalt)
    with pytest.raises(ValueError):
        hash_password("test")

from unittest.mock import patch

def test_generate_verification_token():
    """Test the verification token generation."""
    with patch('secrets.token_urlsafe', return_value="mocked_token_value") as mock_token:
        token = generate_verification_token()
        mock_token.assert_called_once_with(16)  # Ensure it's called with the expected parameter
        assert token == "mocked_token_value", "The token should match the mocked value."

@pytest.mark.parametrize("special_password", [
    "!@#$$%^&*()_+-=[]{}|;':,.<>?/~`",  # Symbols
    "P@$$w0rd💖",  # Password with emoji
    "パスワード123",  # Unicode characters
])

def test_password_with_special_characters(special_password):
    """Test password hashing and verification with special characters."""
    hashed = hash_password(special_password)
    assert isinstance(hashed, str) and hashed.startswith('$2b$'), "Hashed password should be bcrypt format."
    assert verify_password(special_password, hashed) is True, "Password with special characters should match the hash."
    assert verify_password("incorrect_password", hashed) is False, "Incorrect password should not match the hash."

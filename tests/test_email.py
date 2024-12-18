import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.email_service import EmailService
from app.utils.template_manager import TemplateManager

    
@pytest.mark.asyncio
async def test_send_markdown_email(email_service):
    """Test sending markdown email with user data."""
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "verification_url": "http://example.com/verify?token=abc123"
    }
    await email_service.send_user_email(user_data, 'email_verification')

    # Assert the SMTP client is called correctly
    email_service.smtp_client.send_email.assert_called_once_with(
        "Verify Your Account", "<html>Email Content</html>", "test@example.com"
    )

    # Assert the template manager renders the template with the right data
    email_service.template_manager.render_template.assert_called_once_with(
        "email_verification", **user_data
    )

@pytest.mark.asyncio
async def test_send_user_email_missing_data(email_service):
    """Test sending an email with missing user data keys."""
    incomplete_user_data = {"email": "test@example.com"}  # Missing 'name' and 'verification_url'
    with pytest.raises(KeyError, match=".*name.*"):
        await email_service.send_user_email(incomplete_user_data, 'email_verification')

@pytest.mark.asyncio
async def test_send_user_email_invalid_email_type(email_service):
    """Test sending an email with an invalid email type."""
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "verification_url": "http://example.com/verify?token=abc123"
    }
    with pytest.raises(ValueError, match="Invalid email type"):
        await email_service.send_user_email(user_data, "invalid_type")
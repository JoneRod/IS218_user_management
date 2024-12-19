import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.email_service import EmailService
from app.utils.template_manager import TemplateManager

    
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_send_markdown_email():
    """Test sending markdown email with user data."""
    # Mock TemplateManager
    template_manager_mock = AsyncMock()
    template_manager_mock.render_template.return_value = "<html>Email Content</html>"

    # Mock EmailService with a mocked SMTP client
    smtp_client_mock = AsyncMock()
    email_service = EmailService(template_manager=template_manager_mock)
    email_service.smtp_client = smtp_client_mock

    # Test data
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "verification_url": "http://example.com/verify?token=abc123"
    }

    # Call the method
    await email_service.send_user_email(user_data, 'email_verification')

    # Assert the SMTP client was called with correct arguments
    smtp_client_mock.send_email.assert_called_once_with(
        "Verify Your Account",
        "<html>Email Content</html>",
        "test@example.com"
    )


@pytest.mark.asyncio
async def test_send_user_email_missing_data(email_service):
    """Test sending an email with missing user data keys."""
    incomplete_user_data = {"email": "test@example.com"}  # Missing 'name' and 'verification_url'

    # Mock the template_manager and its render_template method
    email_service.template_manager = AsyncMock()
    email_service.template_manager.render_template.side_effect = KeyError("name")

    with pytest.raises(KeyError, match="name"):
        await email_service.send_user_email(incomplete_user_data, 'email_verification')


@pytest.mark.asyncio
async def test_send_user_email_invalid_email_type():
    """Test sending an email with an invalid email type."""
    template_manager = TemplateManager()  # Initialize the real TemplateManager or mock it if needed
    email_service = EmailService(template_manager)  # Use the real EmailService
    
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "verification_url": "http://example.com/verify?token=abc123"
    }

    with pytest.raises(ValueError, match="Invalid email type"):
        await email_service.send_user_email(user_data, 'invalid_email_type')

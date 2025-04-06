"""
Tests for the Webmotors API authentication functionality using real API calls.
"""

import os
import logging
import sys
import pytest
from dotenv import load_dotenv

from src.services.webmotors.client import WebmotorsClient

# Configure logging to output to stdout
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Get the root logger and add the handler
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(handler)

# Load environment variables for tests
load_dotenv()

@pytest.fixture
def client():
    """Create a WebmotorsClient instance for testing."""
    return WebmotorsClient()

def test_auth_with_env_credentials(client):
    """Test authentication using credentials from environment variables."""
    # Log environment variables (masked)
    print("\nTesting with environment variables:")
    print(f"Client ID: {os.getenv('WEBMOTORS_CLIENT_ID', '')[:4]}...{os.getenv('WEBMOTORS_CLIENT_ID', '')[-4:]}")
    print(f"Client Secret: {os.getenv('WEBMOTORS_CLIENT_SECRET', '')[:4]}...{os.getenv('WEBMOTORS_CLIENT_SECRET', '')[-4:]}")
    print(f"API Username: {os.getenv('WEBMOTORS_API_USERNAME', '')[:4]}...{os.getenv('WEBMOTORS_API_USERNAME', '')[-4:]}")
    print(f"API Password: {'*' * 8 if os.getenv('WEBMOTORS_API_PASSWORD') else None}")
    
    # This test assumes valid credentials are set in .env file
    result = client.authenticate()
    
    assert result is True
    assert client.access_token is not None
    assert isinstance(client.access_token, str)
    assert len(client.access_token) > 0

def test_auth_with_explicit_credentials():
    """Test authentication using explicitly provided credentials."""
    # Use environment variables as explicit credentials
    client_id = os.getenv("WEBMOTORS_CLIENT_ID")
    client_secret = os.getenv("WEBMOTORS_CLIENT_SECRET")
    api_username = os.getenv("WEBMOTORS_API_USERNAME")
    api_password = os.getenv("WEBMOTORS_API_PASSWORD")
    
    if not all([client_id, client_secret, api_username, api_password]):
        pytest.skip("Skipping test: No credentials found in environment variables")
    
    # Log credentials being used (masked)
    print("\nTesting with explicit credentials:")
    print(f"Client ID: {client_id[:4]}...{client_id[-4:]}")
    print(f"Client Secret: {client_secret[:4]}...{client_secret[-4:]}")
    print(f"API Username: {api_username[:4]}...{api_username[-4:]}")
    print(f"API Password: {'*' * 8}")
    
    client = WebmotorsClient(
        client_id=client_id,
        client_secret=client_secret,
        api_username=api_username,
        api_password=api_password
    )
    
    result = client.authenticate()
    
    assert result is True
    assert client.access_token is not None
    assert isinstance(client.access_token, str)
    assert len(client.access_token) > 0

def test_auth_with_invalid_credentials():
    """Test authentication fails with invalid credentials."""
    client = WebmotorsClient(
        client_id="invalid_client_id",
        client_secret="invalid_client_secret",
        api_username="invalid_username",
        api_password="invalid_password"
    )
    
    result = client.authenticate()
    
    assert result is False
    assert client.access_token is None 
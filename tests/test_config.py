"""
Tests for configuration module.

Tests environment variable loading and validation.
"""

import pytest
import os
from pathlib import Path
from unittest.mock import patch

from src.utils.config import Config


class TestConfig:
    """Test cases for Config class."""

    def test_config_loads_env_variables(self):
        """Test that Config loads environment variables correctly."""
        # This test assumes .env file exists with valid credentials
        config = Config()

        assert config.access_key is not None
        assert config.secret_key is not None
        assert config.partner_id is not None
        assert config.api_base_url == "https://api-gateway.coupang.com"

    def test_config_validates_required_fields(self):
        """Test that Config raises error when required fields are missing."""
        # Mock both os.environ and load_dotenv to prevent loading .env file
        with patch.dict(os.environ, {}, clear=True):
            with patch('src.utils.config.load_dotenv'):
                with pytest.raises(ValueError) as exc_info:
                    Config()

                error_message = str(exc_info.value)
                assert "COUPANG_ACCESS_KEY" in error_message
                assert "COUPANG_SECRET_KEY" in error_message
                assert "COUPANG_PARTNER_ID" in error_message

    def test_config_repr_hides_sensitive_data(self):
        """Test that Config.__repr__ does not expose sensitive data."""
        config = Config()
        repr_str = repr(config)

        # Should contain asterisks instead of actual keys
        assert "********" in repr_str or "access_key" in repr_str
        # Should not contain actual secret key value
        assert config.secret_key not in repr_str
        # Should contain partner_id (not sensitive)
        assert config.partner_id in repr_str

    def test_config_partial_missing_variables(self):
        """Test that Config fails when only some variables are present."""
        # Mock environment with only access_key and prevent loading .env file
        with patch.dict(os.environ, {"COUPANG_ACCESS_KEY": "test_key"}, clear=True):
            with patch('src.utils.config.load_dotenv'):
                with pytest.raises(ValueError) as exc_info:
                    Config()

                error_message = str(exc_info.value)
                assert "COUPANG_SECRET_KEY" in error_message
                assert "COUPANG_PARTNER_ID" in error_message
                # ACCESS_KEY should not be in missing list
                assert "COUPANG_ACCESS_KEY" not in error_message

    def test_config_env_file_path(self):
        """Test that Config looks for .env in correct location."""
        config = Config()

        # Verify that config has loaded values (which means .env was found)
        assert config.access_key is not None

    @patch.dict(os.environ, {
        "COUPANG_ACCESS_KEY": "test_access",
        "COUPANG_SECRET_KEY": "test_secret",
        "COUPANG_PARTNER_ID": "test_partner"
    })
    def test_config_with_mocked_env(self):
        """Test Config with mocked environment variables."""
        config = Config()

        assert config.access_key == "test_access"
        assert config.secret_key == "test_secret"
        assert config.partner_id == "test_partner"

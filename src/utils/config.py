"""
Configuration management for Coupang MCP Server.

Loads environment variables and provides configuration settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional


class Config:
    """Configuration class for Coupang API credentials and settings."""

    def __init__(self):
        """Initialize configuration by loading environment variables."""
        # Load .env file from project root
        env_path = Path(__file__).parent.parent.parent / ".env"
        load_dotenv(env_path)

        # Load Coupang API credentials
        self.access_key: Optional[str] = os.getenv("COUPANG_ACCESS_KEY")
        self.secret_key: Optional[str] = os.getenv("COUPANG_SECRET_KEY")
        self.partner_id: Optional[str] = os.getenv("COUPANG_PARTNER_ID")
        self.sub_id: Optional[str] = os.getenv("COUPANG_SUB_ID")  # Optional tracking ID

        # API base URL
        self.api_base_url: str = "https://api-gateway.coupang.com"

        # Validate required credentials
        self._validate()

    def _validate(self) -> None:
        """Validate that all required credentials are present."""
        missing = []

        if not self.access_key:
            missing.append("COUPANG_ACCESS_KEY")
        if not self.secret_key:
            missing.append("COUPANG_SECRET_KEY")
        if not self.partner_id:
            missing.append("COUPANG_PARTNER_ID")

        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}. "
                f"Please check your .env file."
            )

    def __repr__(self) -> str:
        """String representation (hides sensitive data)."""
        return (
            f"Config(access_key={'*' * 8 if self.access_key else None}, "
            f"secret_key={'*' * 8 if self.secret_key else None}, "
            f"partner_id={self.partner_id})"
        )


# Global config instance
config = Config()

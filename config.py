import os
from dotenv import load_dotenv

load_dotenv()

class ConfigError(Exception):
    """Custom exception for configuration errors in Storyblok MCP"""
    pass

class Config:
    """
    Loads and validates Storyblok configuration from environment variables.
    Raises ConfigError if any required variable is missing.
    Attributes:
        space_id (str): Storyblok space ID.
        management_token (str): Storyblok management API token.
        public_token (str): Storyblok default public API token.
    """
    def __init__(self):
        """Initializes Config and validates required environment variables."""
        self.space_id = os.getenv("STORYBLOK_SPACE_ID")
        self.management_token = os.getenv("STORYBLOK_MANAGEMENT_TOKEN")
        self.public_token = os.getenv("STORYBLOK_DEFAULT_PUBLIC_TOKEN")

        if not self.space_id:
            raise ConfigError("STORYBLOK_SPACE_ID is missing.")
        if not self.management_token:
            raise ConfigError("STORYBLOK_MANAGEMENT_TOKEN is missing.")
        if not self.public_token:
            raise ConfigError("STORYBLOK_DEFAULT_PUBLIC_TOKEN is missing.")

API_ENDPOINTS = {
    "MANAGEMENT": "https://mapi.storyblok.com/v1"
}

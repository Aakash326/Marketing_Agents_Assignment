"""
Configuration management for LangGraph Backend API.

Manages environment variables, API keys, and application settings.
"""

import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "Portfolio Intelligence API (LangGraph)"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False)
    ENVIRONMENT: str = Field(default="development")

    # Server
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    RELOAD: bool = Field(default=True)

    # CORS
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173", "http://localhost:8080"]
    )
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = Field(default=["*"])
    CORS_ALLOW_HEADERS: List[str] = Field(default=["*"])

    # API Keys
    OPENAI_API_KEY: str = Field(...)
    ALPHA_VANTAGE_API_KEY: str = Field(default="")
    TAVILY_API_KEY: str = Field(default="")

    # Portfolio Data
    PORTFOLIO_FILE_PATH: str = Field(default="portfolios.xlsx")

    # LangGraph Settings
    MAX_WORKFLOW_ITERATIONS: int = Field(default=10)
    WORKFLOW_TIMEOUT: int = Field(default=300)  # seconds

    # Logging
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FORMAT: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = Field(default=True)
    RATE_LIMIT_PER_MINUTE: int = Field(default=60)

    # API Authentication (optional)
    API_KEY_ENABLED: bool = Field(default=False)
    API_KEY: str = Field(default="")

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"


# Global settings instance
settings = Settings()


def validate_settings():
    """
    Validate critical settings on startup.

    Raises:
        ValueError: If critical settings are missing or invalid
    """
    errors = []

    # Check OpenAI API key
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your_openai_api_key_here":
        errors.append("OPENAI_API_KEY is not set or is using default value")

    # Check portfolio file exists
    if not os.path.exists(settings.PORTFOLIO_FILE_PATH):
        errors.append(f"Portfolio file not found: {settings.PORTFOLIO_FILE_PATH}")

    # Validate timeout
    if settings.WORKFLOW_TIMEOUT <= 0:
        errors.append("WORKFLOW_TIMEOUT must be positive")

    if errors:
        raise ValueError(f"Configuration errors:\n" + "\n".join(f"  - {e}" for e in errors))


def get_settings() -> Settings:
    """Get the global settings instance."""
    return settings

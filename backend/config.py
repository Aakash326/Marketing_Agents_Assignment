"""
Configuration settings for the Portfolio Intelligence API.
Uses pydantic-settings for environment variable management.
"""

from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Portfolio Intelligence API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Multi-agent portfolio and market intelligence system"
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True  # Set to False in production
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: List[str] = ["*"]  # Configure properly in production
    
    # Session Management
    SESSION_CLEANUP_HOURS: int = 24
    MAX_CONVERSATION_HISTORY: int = 10  # Keep last 5 Q&A pairs (10 messages)
    
    # OpenAI API (loaded from .env)
    OPENAI_API_KEY: Optional[str] = None
    
    # Portfolio Data
    PORTFOLIO_FILE: str = "portfolios.xlsx"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

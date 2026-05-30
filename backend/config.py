"""
Configuration management for MNIST Classifier API.
Loads settings from environment variables with sensible defaults.
"""

import os
from typing import Optional

class Config:
    """API Configuration settings."""
    
    # API Settings
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_RELOAD: bool = os.getenv("API_RELOAD", "True").lower() == "true"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Model Settings
    MODEL_TYPE: str = os.getenv("MODEL_TYPE", "final")
    MODEL_PATH: str = os.getenv("MODEL_PATH", "./models/final_model.pkl")
    
    # CORS Settings
    CORS_ORIGINS: list = ["*"]
    CORS_CREDENTIALS: bool = os.getenv("CORS_CREDENTIALS", "True").lower() == "true"
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: Optional[str] = os.getenv("LOG_FILE", "api.log")
    
    # Security
    RATE_LIMIT_ENABLED: bool = os.getenv("RATE_LIMIT_ENABLED", "True").lower() == "true"
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "60"))
    
    # Performance
    ENABLE_CACHE: bool = os.getenv("ENABLE_CACHE", "True").lower() == "true"
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))
    
    # Input Validation
    EXPECTED_PIXEL_COUNT: int = 784
    MIN_PIXEL_VALUE: float = 0.0
    MAX_PIXEL_VALUE: float = 1.0
    
    @classmethod
    def get_settings(cls) -> dict:
        """Return all settings as a dictionary."""
        return {
            "api_host": cls.API_HOST,
            "api_port": cls.API_PORT,
            "debug": cls.DEBUG,
            "model_type": cls.MODEL_TYPE,
            "logging_level": cls.LOG_LEVEL,
        }


# Global config instance
config = Config()

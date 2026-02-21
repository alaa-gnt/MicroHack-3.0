"""
Application settings using pydantic-settings
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    
    # Scraping Settings
    SCRAPE_INTERVAL_MINUTES: int = Field(default=300, description="Scrape interval in minutes (5 hours)")
    
    # Redis Settings
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)
    REDIS_DB: int = Field(default=0)
    REDIS_PASSWORD: Optional[str] = Field(default=None)
    
    # RabbitMQ Settings
    RABBITMQ_HOST: str = Field(default="localhost")
    RABBITMQ_PORT: int = Field(default=5672)
    RABBITMQ_USER: str = Field(default="guest")
    RABBITMQ_PASSWORD: str = Field(default="guest")
    RABBITMQ_QUEUE: str = Field(default="scraping_signals")
    
    # MinIO/S3 Settings
    MINIO_ENDPOINT: str = Field(default="localhost:9000")
    MINIO_ACCESS_KEY: str = Field(default="minioadmin")
    MINIO_SECRET_KEY: str = Field(default="minioadmin")
    MINIO_BUCKET: str = Field(default="scraping-data")
    MINIO_SECURE: bool = Field(default=False)
    
    # API Keys
    LENS_API_KEY: Optional[str] = Field(default=None)
    IEEE_API_KEY: Optional[str] = Field(default=None)
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"


# Global settings instance
settings = Settings()

# Export SCRAPE_INTERVAL_MINUTES for backward compatibility
SCRAPE_INTERVAL_MINUTES = settings.SCRAPE_INTERVAL_MINUTES

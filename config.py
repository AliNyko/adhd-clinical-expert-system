"""Configuration settings for the ADHD Clinical Expert System."""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings and configuration."""
    
    # Application
    APP_NAME: str = "ADHD Clinical Expert System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "sqlite:///./adhd_expert_system.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Clinical Thresholds
    ASRS_CUTOFF: int = 4  # Part A significant symptoms
    PHQ9_MILD: int = 5
    PHQ9_MODERATE: int = 10
    PHQ9_SEVERE: int = 15
    GAD7_MILD: int = 5
    GAD7_MODERATE: int = 10
    GAD7_SEVERE: int = 15
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
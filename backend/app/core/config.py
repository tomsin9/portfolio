from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union

class Settings(BaseSettings):
    PROJECT_NAME: str = "Personal Website"
    DATABASE_URL: str
    DEBUG: bool = False
    PORT: int = 8000
    
    # Admin settings
    ADMIN_DOCS_URL: str = "/admin"
    API_ADMIN_USERNAME: str
    API_ADMIN_PASSWORD: str
    
    # JWT settings
    JWT_SECRET_KEY: str = "your-long-random-hex-string" 
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    
    # Comma-separated; dev (Vite :5173) + prod (e.g. nginx :80 on localhost)
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost,http://127.0.0.1"
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding='utf-8',
        extra="ignore" # Ignore extra variables to reduce errors
    )
    
    @property
    def origins_list(self) -> list[str]:
        return [item.strip() for item in self.ALLOWED_ORIGINS.split(",")]

settings = Settings()
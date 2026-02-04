from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union

class Settings(BaseSettings):
    PROJECT_NAME: str = "Portfolio Website"
    DATABASE_URL: str
    DEBUG: bool = False
    PORT: int = 8000
    API_ADMIN_USERNAME: str
    API_ADMIN_PASSWORD: str
    
    ALLOWED_ORIGINS: str = "http://localhost:5173"
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding='utf-8',
        extra="ignore" # 忽略多餘的變數，減少報錯
    )
    
    @property
    def origins_list(self) -> list[str]:
        return [item.strip() for item in self.ALLOWED_ORIGINS.split(",")]

# 3. 實例化
settings = Settings()
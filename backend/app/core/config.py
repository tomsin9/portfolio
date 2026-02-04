from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # 1. 定義變數名同 Type
    PROJECT_NAME: str = "My Portfolio"
    DATABASE_URL: str
    DEBUG: bool = False
    PORT: int = 8000
    
    # 2. 設定讀取來源
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

# 3. 實例化
settings = Settings()
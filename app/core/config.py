from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    PRIVATE_KEY_PATH: Path
    PUBLIC_KEY_PATH: Path
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

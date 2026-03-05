from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = None
    SECRET_KEY: str = None
    ALGORITHM: str = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int = None

    class Config:
        env_file = ".env"

settings = Settings()
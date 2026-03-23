from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str | None = None
    SECRET_KEY: str | None = None
    ALGORITHM: str | None = None
<<<<<<< HEAD
    ACCESS_TOKEN_EXPIRE_MINUTES: int | None = 30
=======
    ACCESS_TOKEN_EXPIRE_MINUTES: int 
>>>>>>> 584815ab66c351d7ac8a53fa402fc651fd90d8b4

    UPLOAD_DIR: str = "/app/uploads"
    MEDIA_URL_PREFIX: str = "/media"
    MAX_IMAGE_SIZE: int = 10 * 1024 * 1024  # 10 MB
    ALLOWED_IMAGE_MIME_TYPES: dict[str, str] = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
    }

    class Config:
        env_file = ".env"


settings = Settings()
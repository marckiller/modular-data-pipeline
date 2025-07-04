from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    ADMIN_API_KEY: str
    SECRET_KEY: str = "changeme"
    DEBUG: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@db:5432/cookiemanager"
    SECRET_KEY: str = "artutos123"
    FRONTEND_URL: str = "http://frontend:3000"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 horas
    DEFAULT_USER_EMAIL: str = "admin@artutos.eu.org"
    DEFAULT_USER_PASSWORD: str = "artutos123"

    class Config:
        env_file = ".env"

settings = Settings()
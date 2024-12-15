from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@db:5432/cookiemanager"
    SECRET_KEY: str = "your-secret-key-here"
    FRONTEND_URL: str = "http://84.46.249.121"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    class Config:
        env_file = ".env"

settings = Settings()
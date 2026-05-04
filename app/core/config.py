from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "cultural_events_db"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "1"

    OPENAI_API_KEY: str | None = None

    @property
    def DATABASE_URL(self) -> str:
        database_url = os.getenv("DATABASE_URL")

        # 👉 если есть Render DB — используем её
        if database_url:
            return database_url.replace("postgresql://", "postgresql+asyncpg://")

        # 👉 если нет (локально) — используем старую
        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"


settings = Settings()
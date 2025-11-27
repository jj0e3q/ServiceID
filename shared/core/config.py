from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class BaseAppSettings(BaseSettings):
    ENV: str = "local"

    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "pass123"
    POSTGRES_DB: str = "main"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    JWT_KEYS_DIR: str = "/keys"
    JWT_ALGORITHM: str = "RS256"

    @property
    def database_url(self) -> str:
        return str(PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        ))

    @property
    def jwt_keys_path(self) -> Path:
        return Path(self.JWT_KEYS_DIR)

    class Config:
        env_file = ".env"
        case_sensitive = True
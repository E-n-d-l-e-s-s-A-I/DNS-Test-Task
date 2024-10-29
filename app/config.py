from typing import Literal
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    ECHO: bool
    DB_STR_MAX_LEN: int = 255

    TEST_POSTGRES_DB: str
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str
    TEST_DB_HOST: str
    TEST_DB_PORT: int

    model_config = ConfigDict(env_file="envs/.env")

    @property
    def DATABASE_URL(self):
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.DB_HOST}:"
            f"{self.DB_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def TEST_DATABASE_URL(self):
        return (
            f"postgresql+asyncpg://{self.TEST_POSTGRES_USER}:"
            f"{self.TEST_POSTGRES_PASSWORD}@{self.TEST_DB_HOST}:"
            f"{self.TEST_DB_PORT}/{self.TEST_POSTGRES_DB}"
        )


settings = Settings()

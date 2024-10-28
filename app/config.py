from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    ECHO: bool
    DB_STR_MAX_LEN: int = 255

    class Config:
        env_file = ".env"

    @property
    def DATABASE_URL(self):
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()

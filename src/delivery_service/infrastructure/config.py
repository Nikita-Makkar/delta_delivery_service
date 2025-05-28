from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings.
    """

    # App
    ENVIRONMENT: Literal["DEV", "PROD", "TEST"] = "DEV"
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = (
        "ERROR"
    )

    # MySQL
    MYSQL_HOST: str = ""
    MYSQL_PORT: int = 0
    MYSQL_ROOT_PASSWORD: str = ""
    MYSQL_DATABASE: str = ""
    MYSQL_USER: str = ""
    MYSQL_PASSWORD: str = ""

    # RabbitMQ
    RABBITMQ_URL: str = ""
    RABBITMQ_DEFAULT_USER: str = ""
    RABBITMQ_DEFAULT_PASS: str = ""

    # Redis
    REDIS_HOST: str = ""
    REDIS_PORT: str = ""
    REDIS_TTL: str = ""

    @property
    def DB_URL(self) -> str:
        """
        Builds full async DB connection string.
        """
        return (
            f"mysql+asyncmy://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@"
            f"{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
        )

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

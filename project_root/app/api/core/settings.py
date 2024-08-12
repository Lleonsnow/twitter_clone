import os

from dotenv import load_dotenv
from pydantic import ConfigDict, SecretStr, StrictStr
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Конфигурация приложения."""

    model_config = ConfigDict(extra="ignore")
    pg_user: SecretStr = os.getenv("POSTGRES_USER", None)
    pg_password: SecretStr = os.getenv("POSTGRES_PASSWORD", None)
    base_url: SecretStr = os.getenv("DATABASE_URL", None)
    project_name: StrictStr = os.getenv("PROJECT_NAME", None)
    project_version: StrictStr = os.getenv("PROJECT_VERSION", None)
    sentry_dsn: SecretStr = os.getenv("SENTRY_DSN", None)

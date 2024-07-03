import os
from dotenv import load_dotenv
from pydantic import SecretStr, StrictStr, ConfigDict
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    model_config = ConfigDict(extra="ignore")

    api_key: SecretStr = os.getenv("API_KEY", None)
    pg_user: SecretStr = os.getenv("POSTGRES_USER", None)
    pg_password: SecretStr = os.getenv("POSTGRES_PASSWORD", None)
    base_url: SecretStr = os.getenv("DATABASE_URL", None)
    project_name: StrictStr = os.getenv("PROJECT_NAME", None)
    project_version: StrictStr = os.getenv("PROJECT_VERSION", None)
    db_test: SecretStr = os.getenv("DAT", None)
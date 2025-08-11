from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = Path(__file__).resolve().parent.parent.parent / ".env"


class Config(BaseSettings):
    # Database
    DB_URL: str

    SECRET_KEY: str
    ALGORITHM: str

    EMAIL_HOST_USER: str
    EMAIL_HOST_PASSWORD: str
    SMTP_HOST: str
    SMTP_PORT: int

    model_config = SettingsConfigDict(env_file=DOTENV)


config = Config()

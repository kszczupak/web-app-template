from enum import StrEnum
from pathlib import Path

from pydantic import PostgresDsn
from pydantic import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Environment(StrEnum):
    DEV = "dev"
    PROD = "prod"


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    environment: Environment

    DB_USERNAME: str
    DB_DATABASE: str
    DB_PORT: int = 5432
    DB_PASSWORD: str
    DB_HOST: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def sqlalchemy_database_uri(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.DB_USERNAME,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.DB_DATABASE,
        )

    @computed_field
    @property
    def app_dir(self) -> Path:
        return Path(__file__).parent.resolve()

    @computed_field
    @property
    def static_dir(self) -> Path:
        """
        Path to static files (CSS, JS, images, etc.), generated mostly by Vite, during the build.
        In development, static files are served by vite dev server that allows hot reloading.
        """
        return self.app_dir / "static"

    @computed_field
    @property
    def templates_dir(self) -> Path:
        return self.app_dir / "templates"


config = Config()

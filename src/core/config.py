from logging import config as logging_config
from pathlib import Path

from pydantic.v1 import BaseSettings

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class AppSettings(BaseSettings):
    app_title: str = "ratevid"
    database_dsn: str
    host: str = "0.0.0.0"
    port: int = 8000
    base_dir: Path = Path(__file__).parent.parent

    class Config:
        env_file = ".dev-only-env"


app_settings = AppSettings()

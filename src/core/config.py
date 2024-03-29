from logging import config as logging_config
from pathlib import Path

from pydantic.v1 import BaseSettings

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class AppSettings(BaseSettings):
    app_title: str = "ratevid"
    host: str = "0.0.0.0"
    port: int = 8000
    database_dsn: str
    base_dir: Path = Path(__file__).parent.parent
    base_currency: str = "USD"
    exchange_rate_api_url: str
    exchange_rate_api_key: str

    class Config:
        env_file = ".dev-only-env"


app_settings = AppSettings()

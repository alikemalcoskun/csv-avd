from starlette.config import Config
from pydantic_settings import BaseSettings

config = Config(".env")

class Cfg(BaseSettings):
    APP_NAME: str = "Multi-Agent CSV Data Analysis API"
    APP_VERSION: str = "0.0.1"
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = config("DEBUG", cast=bool, default=False)


cfg = Cfg()

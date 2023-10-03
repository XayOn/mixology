from pydantic_settings import BaseSettings


class InitSettings(BaseSettings):
    db_uri: str = "sqlite:///./db.sqlite3"


Settings = InitSettings()

from pydantic_settings import BaseSettings, SettingsConfigDict


class InitSettings(BaseSettings):
    mongodb_url: str = "mongodb://localhost:27017"
    mqtt_host: str = "localhost"
    mqtt_port: int = 18917
    redis_url: str = "redis://localhost:6379/1"
    public_url: str = "http://localhost/"
    model_config = SettingsConfigDict(env_file=".env")


Settings = InitSettings()

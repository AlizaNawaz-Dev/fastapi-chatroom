from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expiry_minutes: int
    redis_host: str
    redis_port: int
    redis_db: int
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

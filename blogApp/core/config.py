from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    app_name: str = "FastAPI App"
    environment: str = "development"

    # Database
    database_url: str
    test_database_url: str | None = None

    # Security
    access_secret_key: str
    refresh_secret_key: str
    algorithm: str = "HS256"

    # Token expiry (minutes)
    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 10080

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8"
    )


settings = Settings()

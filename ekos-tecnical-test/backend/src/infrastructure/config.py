from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    anthropic_api_key: str
    database_url: str
    tavily_api_key: str = ""
    app_secret_key: str
    app_env: str = "development"
    app_port: int = 8000
    frontend_url: str = "http://localhost:3000"
    sendgrid_api_key: str = ""
    support_email: str = ""

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


settings = Settings()

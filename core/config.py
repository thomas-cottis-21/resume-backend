from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str = "mysql+aiomysql://root:root@localhost:3306/nomadica"
    app_env: str = "development"
    log_level: str = "INFO"
    cors_origins_raw: str = Field(
        default="http://localhost:3000,http://localhost:5173",
        alias="CORS_ORIGINS",
    )

    # JWT
    jwt_secret: str = Field(alias="JWT_SECRET")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30

    # Google OAuth2
    google_client_id: str = Field(alias="GOOGLE_CLIENT_ID")
    google_client_secret: str = Field(alias="GOOGLE_CLIENT_SECRET")
    google_redirect_uri: str = Field(alias="GOOGLE_REDIRECT_URI")
    google_auth_url: str = "https://accounts.google.com/o/oauth2/v2/auth"
    google_token_url: str = "https://oauth2.googleapis.com/token"
    google_userinfo_url: str = "https://www.googleapis.com/oauth2/v3/userinfo"
    oauth_success_redirect: str = Field(
        default="http://localhost:5173/oauth/callback",
        alias="OAUTH_SUCCESS_REDIRECT",
    )

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins_raw.split(",")]


settings = Settings()

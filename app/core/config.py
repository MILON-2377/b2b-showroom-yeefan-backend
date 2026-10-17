from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

CookieSameSite = Literal["lax", "strict", "none"]


class Settings(BaseSettings):
    # Database
    database_url: str

    # Jwt
    jwt_secret_key: str
    jwt_algorithm: str = "SHA256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    session_expire_days: int = 30
    max_sessions_per_user: int = 2

    # Cookie
    access_token_cookie_name: str = "__Host-access_token"
    refresh_token_cookie_name: str = "__Secure-refresh_token"

    access_token_cookie_path: str = "/"
    refresh_token_cookie_path: str = "/api/v1/auth"

    auth_cookie_httponly: bool = True
    auth_cookie_secure: bool = True
    auth_cookie_samesite: str = "lax"

    # Storage
    storage_root: str = "./storage"

    cloudinary_cloud_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str
    cloudinary_upload_preset: str

    # Cors
    cors_origins: list[str] = [
        "http://localhost:3000",
    ]


    # Email
    brevo_api_key: str
    brevo_sender_email: str
    brevo_sender_name: str = "YIFAN BRIDAL"

    # Ai
    deepseek_api_key: str
    deepseek_base_url: str = "https://api.deepseek.com"
    deepseek_model: str = "deepseek-flash"

    # Open Router
    openrouter_api_key: str
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "openrouter/free"

    # Kaggle
    ollama_base_url: str = "http://localhost:11434/v1"
    ollama_api_key: str = "ollama"
    ollama_model: str = "deepseek-r1:14b"

    ai_provider: str = "ollama"

    LOG_LEVEL: str = "INFO"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()

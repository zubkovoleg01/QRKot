# app/core/config.py
from typing import Optional

from pydantic import EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Класс для хранения настроек приложения."""

    app_title: str = 'FastAPI Application'
    """Название приложения."""

    app_description: str = 'FastAPI application description'
    """Описание приложения."""

    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    """URL базы данных."""

    secret: str = 'SecretKey'
    """Секретный ключ приложения."""

    first_superuser_email: Optional[EmailStr] = None
    """Email первого суперпользователя."""

    first_superuser_password: Optional[str] = None
    """Пароль первого суперпользователя."""

    class Config:
        env_file = '.env'


settings = Settings()
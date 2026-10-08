"""
Configurações centralizadas do DataMind AI Studio.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Nome e versão da aplicação.
    app_name: str = "DataMind AI Studio"
    app_version: str = "0.1.0"

    # Ambiente de execução.
    environment: str = "development"

    # URL padrão para execução local no Windows.
    # No Docker Compose, o valor será sobrescrito para usar o serviço postgres.
    database_url: str = (
        "postgresql+psycopg://datamind:datamind_dev"
        "@localhost:5433/datamind"
    )

    # Carrega configurações do arquivo .env.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# Instância compartilhada das configurações.
settings = Settings()
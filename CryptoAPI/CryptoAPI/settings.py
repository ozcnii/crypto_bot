# from pathlib import Path

# from pydantic import BaseSettings, BaseSettingsDict


# class Settings(BaseSettings):
#     app_name: str = "Example API"
#     app_host: str = "0.0.0.0"
#     app_port: int = 8080

#     database_url: str = "postgresql+asyncpg://cryptouser:password@localhost:5432/cryptodatabase"

#     project_root: Path = Path(__file__).parent.parent.resolve()

#     model_config = SettingsConfigDict(env_file=".env")


# settings = Settings()
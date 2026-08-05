from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  # --- ENVIRONMENT VARIABLES ---
  DATABASE_URL: str
  POSTGRES_USER: str
  POSTGRES_PASSWORD: str
  POSTGRES_DB: str

  PGADMIN_DEFAULT_EMAIL: str
  PGADMIN_DEFAULT_PASSWORD: str

  SECRET_KEY: str
  ALGORITHM: str

  model_config = SettingsConfigDict(
    env_file=".env", env_file_encoding = 'utf-8', extra="ignore"
  )

settings = Settings()

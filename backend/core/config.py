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

  RABBITMQ_USER: str
  RABBITMQ_PASSWORD: str
  RABBITMQ_HOST: str
  RABBITMQ_PORT: int = 5672
  RABBITMQ_QUEUE: str

  REDIS_HOST: str = "localhost"
  REDIS_PORT: int = 6379

  model_config = SettingsConfigDict(
    env_file=".env", env_file_encoding = 'utf-8', extra="ignore"
  )

settings = Settings()

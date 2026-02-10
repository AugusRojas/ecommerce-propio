from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = 'postgresql+psycopg://postgres:postgres@example.supabase.co:6543/postgres?sslmode=require'
    secret_key: str = 'dev-secret'
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    mercadopago_access_token: str = ''
    cors_origins: str = 'http://localhost:3000'
    db_use_null_pool: bool = True

    model_config = SettingsConfigDict(env_file='.env', case_sensitive=False, extra='ignore')


settings = Settings()

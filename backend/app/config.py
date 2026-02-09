from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = 'sqlite:///./ecommerce.db'
    secret_key: str = 'dev-secret'
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    mercadopago_access_token: str = ''
    cors_origins: str = 'http://localhost:3000'

    class Config:
        env_file = '.env'

settings = Settings()

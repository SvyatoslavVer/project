import os
#from pydantic import BaseSettings
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    DB_HOST: str = os.getenv("DB_HOST", "postgres")
    DB_PORT: int = os.getenv("DB_PORT", 5432)
    DB_NAME: str = os.getenv("DB_NAME", "balances")
    DB_USER: str = os.getenv("DB_USER", "user")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "password")
    ARBITRUM_RPC_URL: str = "https://arb1.arbitrum.io/rpc"

    class Config:
        env_file = ".env"

settings = Settings()

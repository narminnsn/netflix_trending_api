from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB: str
    MYSQL_HOST: str
    MYSQL_PORT: int

    class Config:
        env_file = ".env"

settings = Settings()
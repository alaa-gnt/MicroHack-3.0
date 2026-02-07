from pydantic_settings import BaseSettings
from typing import List, Optional
from pydantic import computed_field


class Settings(BaseSettings):
    PROJECT_NAME: str = "MicroHack Backend"
    API_V1_STR: str = "/api/v1"
    
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "microhack"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: str = "5432"
    
    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

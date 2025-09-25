from pydantic_settings import BaseSettings
from enum import Enum

class StorageType(str, Enum):
    MEMORY = "memory"

class Settings(BaseSettings):
    storage_type: StorageType = StorageType.MEMORY
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
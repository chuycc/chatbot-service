from pydantic_settings import BaseSettings
from enum import Enum

class StorageType(str, Enum):
    MEMORY = "memory"
    FILESYSTEM = "filesystem"

class Settings(BaseSettings):
    storage_type: StorageType = StorageType.MEMORY
    filesystem_storage_path: str = "conversations"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
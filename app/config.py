from pydantic_settings import BaseSettings
import json
from enum import Enum

class StorageType(str, Enum):
    MEMORY = "memory"
    FILESYSTEM = "filesystem"

class LLMType(str, Enum):
    OPENAI = "openai"

class Settings(BaseSettings):
    # Service
    service_timeout: int = 30

    # Storage settings
    storage_type: StorageType = StorageType.MEMORY
    filesystem_storage_path: str = "conversations"

    # LLM settings
    llm_type: LLMType = LLMType.OPENAI
    llm_timeout: int = 30

    # OpenAI settings
    openai_api_key: str = ""
    openai_chat_settings: dict = {
        "model": "gpt-4o"
    }
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

if isinstance(settings.openai_chat_settings, str):
        settings.openai_chat_settings = json.loads(settings.openai_chat_settings)
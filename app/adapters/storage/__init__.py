from .base import StorageAdapter
from .memory import MemoryStorageAdapter

def get_storage_adapter() -> StorageAdapter:
    from app.config import settings, StorageType

    if settings.storage_type == StorageType.MEMORY:
        return MemoryStorageAdapter()
    else:
        raise ValueError(f"Unsupported storage type: {settings.storage_type}")

__all__ = ["StorageAdapter", "MemoryStorageAdapter", "get_storage_adapter"]
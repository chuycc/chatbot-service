from .base import StorageAdapter
from .memory import MemoryStorageAdapter
from .filesystem import FilesystemStorageAdapter

def get_storage_adapter() -> StorageAdapter:
    from app.config import settings, StorageType

    if settings.storage_type == StorageType.MEMORY:
        return MemoryStorageAdapter()
    elif settings.storage_type == StorageType.FILESYSTEM:
        return FilesystemStorageAdapter(settings.filesystem_storage_path)
    else:
        raise ValueError(f"Unsupported storage type: {settings.storage_type}")

__all__ = ["StorageAdapter", "MemoryStorageAdapter", "FilesystemStorageAdapter", "get_storage_adapter"]
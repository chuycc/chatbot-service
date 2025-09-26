from typing import List, Optional, Dict
from .base import StorageAdapter
from app.models.conversation import MessageEntry

class MemoryStorageAdapter(StorageAdapter):
    def __init__(self):
        self._store: Dict[str, List[MessageEntry]] = {}
    
    def add_message(self, conversation_id: str, message: MessageEntry) -> None:
        if conversation_id not in self._store:
            self._store[conversation_id] = []
        self._store[conversation_id].append(message)

    def add_messages(self, conversation_id: str, messages: List[MessageEntry]) -> None:
        if conversation_id not in self._store:
            self._store[conversation_id] = []
        self._store[conversation_id].extend(messages)

    def get_conversation(self, conversation_id: str) -> Optional[List[MessageEntry]]:
        return self._store.get(conversation_id)
    
    def delete_conversation(self, conversation_id: str) -> None:
        if conversation_id in self._store:
            del self._store[conversation_id]

    def conversation_exists(self, conversation_id: str) -> bool:
        return conversation_id in self._store
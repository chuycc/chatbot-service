from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.conversation import MessageEntry

class StorageAdapter(ABC):
    @abstractmethod
    def add_message(self, conversation_id: str, message: MessageEntry) -> None:
        pass
    
    @abstractmethod
    def add_messages(self, conversation_id: str, message: List[MessageEntry]) -> None:
        pass
    
    @abstractmethod
    def get_conversation(self, conversation_id: str) -> Optional[List[MessageEntry]]:
        pass
    
    @abstractmethod
    def delete_conversation(self, conversation_id: str) -> None:
        pass

    @abstractmethod
    def conversation_exists(self, conversation_id: str) -> bool:
        pass
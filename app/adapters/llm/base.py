from abc import ABC, abstractmethod
from typing import List
from app.models.conversation import MessageEntry

class LLMAdapter(ABC):
    @abstractmethod
    async def send_chat_messages(self, messages: List[MessageEntry]) -> str:
        pass
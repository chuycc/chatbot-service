import asyncio
from typing import List
from openai import AsyncOpenAI
from .base import LLMAdapter
from app.models.conversation import MessageEntry, MessageRole

class OpenAIAdapter(LLMAdapter):
    def __init__(self, api_key: str, chat_settings: dict, timeout: int = 30):
        self.client = AsyncOpenAI(api_key=api_key)
        self.chat_settings = chat_settings
        self.timeout = timeout
    
    async def send_chat_messages(self, messages: List[MessageEntry]) -> str:
        openai_messages = self._convert_to_openai_format(messages)

        response = await asyncio.wait_for(
            self.client.chat.completions.create(
                messages=openai_messages,
                **self.chat_settings
            ),
            timeout=self.timeout
        )

        return response.choices[0].message.content
    
    def _convert_to_openai_format(self, messages: List[MessageEntry]) -> List[dict]:
        openai_messages = []
        
        for message in messages:
            message_role = "assistant" if message.role == MessageRole.BOT else "user"
            openai_messages.append({
                "role": message_role,
                "content": message.message
            })

        return openai_messages
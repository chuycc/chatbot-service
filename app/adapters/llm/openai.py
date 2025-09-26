import asyncio
import os
from typing import List, Optional
from openai import AsyncOpenAI
from .base import LLMAdapter
from app.models.conversation import MessageEntry, MessageRole

class OpenAIAdapter(LLMAdapter):
    def __init__(self, api_key: str, chat_settings: dict, timeout: int = 30, system_prompt_path: Optional[str] = None):
        self.client = AsyncOpenAI(api_key=api_key)
        self.chat_settings = chat_settings
        self.timeout = timeout
        self.system_prompt_path = system_prompt_path
    
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
        
        # System prompt
        loaded_prompt = self._load_system_prompt()
        if (loaded_prompt):
            openai_messages.append({
                "role": "system", 
                "content": loaded_prompt
            })

        # Convert conversation messages
        for message in messages:
            message_role = "assistant" if message.role == MessageRole.BOT else "user"
            openai_messages.append({
                "role": message_role,
                "content": message.message
            })
        
        return openai_messages


    
    def _load_system_prompt(self) -> Optional[str]:
        if not self.system_prompt_path:
            return None

        if os.path.exists(self.system_prompt_path):
            try:
                with open(self.system_prompt_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    return content if content else None
            except (IOError, OSError) as e:
                print(f"Warning: Could not read system prompt file {self.system_prompt_path}: {e}")
        return None
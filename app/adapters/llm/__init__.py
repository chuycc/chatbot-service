from .base import LLMAdapter
from .openai import OpenAIAdapter

def get_llm_adapter() -> LLMAdapter:
    from app.config import settings, LLMType
    
    if settings.llm_type == LLMType.OPENAI:
        return OpenAIAdapter(
            api_key=settings.openai_api_key,
            chat_settings=settings.openai_chat_settings,
            timeout=settings.llm_timeout,
            system_prompt_path=settings.llm_system_prompt_path
        )
    else:
        raise ValueError(f"Unsupported LLM type: {settings.llm_type}")

__all__ = ["LLMAdapter", "OpenAIAdapter", "get_llm_adapter"]
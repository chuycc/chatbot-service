import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from app.adapters.llm.openai import OpenAIAdapter
from app.models.conversation import MessageEntry, MessageRole


@pytest.fixture
def openai_adapter():
    api_key = "test-api-key"
    chat_settings = {"model": "gpt-4", "temperature": 0.7}
    return OpenAIAdapter(api_key=api_key, chat_settings=chat_settings, timeout=30)


@pytest.fixture
def sample_messages():
    return [
        MessageEntry(role=MessageRole.USER, message="Hello"),
        MessageEntry(role=MessageRole.BOT, message="Hi there!"),
        MessageEntry(role=MessageRole.USER, message="How are you?")
    ]


class TestOpenAIAdapter:
    def test_convert_to_openai_format(self, openai_adapter, sample_messages):
        result = openai_adapter._convert_to_openai_format(sample_messages)
        
        expected = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
            {"role": "user", "content": "How are you?"}
        ]
        
        assert result == expected

    @pytest.mark.asyncio
    async def test_send_chat_messages_success(self, openai_adapter, sample_messages):
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "This is a response"
        
        with patch.object(openai_adapter.client.chat.completions, 'create', new_callable=AsyncMock) as mock_create:
            mock_create.return_value = mock_response
            
            result = await openai_adapter.send_chat_messages(sample_messages)
            
            assert result == "This is a response"
            mock_create.assert_called_once()

    @pytest.mark.asyncio
    async def test_send_chat_messages_timeout(self, openai_adapter, sample_messages):
        with patch.object(openai_adapter.client.chat.completions, 'create', new_callable=AsyncMock) as mock_create:
            mock_create.side_effect = asyncio.TimeoutError()
            
            with pytest.raises(asyncio.TimeoutError):
                await openai_adapter.send_chat_messages(sample_messages)

    @pytest.mark.asyncio
    async def test_send_chat_messages_general_exception(self, openai_adapter, sample_messages):
        with patch.object(openai_adapter.client.chat.completions, 'create', new_callable=AsyncMock) as mock_create:
            mock_create.side_effect = Exception("API Error")
            
            with pytest.raises(Exception):
                await openai_adapter.send_chat_messages(sample_messages)

    @pytest.mark.asyncio
    async def test_chat_settings_passed_to_api(self, sample_messages):
        chat_settings = {"model": "gpt-4", "temperature": 0.5, "max_tokens": 100}
        adapter = OpenAIAdapter(api_key="test", chat_settings=chat_settings)
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Response"
        
        with patch.object(adapter.client.chat.completions, 'create', new_callable=AsyncMock) as mock_create:
            mock_create.return_value = mock_response
            
            await adapter.send_chat_messages(sample_messages)
            
            mock_create.assert_called_once()
            call_kwargs = mock_create.call_args.kwargs
            
            assert call_kwargs["model"] == "gpt-4"
            assert call_kwargs["temperature"] == 0.5
            assert call_kwargs["max_tokens"] == 100

    def test_empty_messages_list(self, openai_adapter):
        result = openai_adapter._convert_to_openai_format([])
        assert result == []
import pytest
from pydantic import ValidationError
from app.models.conversation import ConversationRequest, MessageEntry, MessageRole

def test_message_entry_valid():
    message = MessageEntry(role=MessageRole.USER, message="Hello!")
    assert message.role == MessageRole.USER
    assert message.message == "Hello!"

def test_message_entry_invalid_role():
    with pytest.raises(ValidationError):
        MessageEntry(role="invalid", message="Hello!")

def test_conversation_request_valid():
    request = ConversationRequest(conversation_id="123", message="Hello!")
    assert request.conversation_id == "123"
    assert request.message == "Hello!"

def test_conversation_request_empty_message():
    with pytest.raises(ValidationError):
        ConversationRequest(conversation_id=None, message="")

def test_conversation_request_long_message():
    with pytest.raises(ValidationError):
        ConversationRequest(conversation_id=None, message="x" * 1001)
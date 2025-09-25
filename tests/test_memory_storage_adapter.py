import pytest
from app.models.conversation import MessageEntry, MessageRole
from app.adapters.storage import MemoryStorageAdapter

@pytest.fixture
def adapter():
    return MemoryStorageAdapter()

@pytest.fixture
def conversation_id():
    return "test-conversation-123"

@pytest.fixture
def message():
    return MessageEntry(role=MessageRole.USER, message="Hello!")

@pytest.fixture
def messages():
    return [
        MessageEntry(role=MessageRole.USER, message="Hello!"),
        MessageEntry(role=MessageRole.BOT, message="Hi there!")
    ]

def test_add_message(adapter, conversation_id, message):
    adapter.add_message(conversation_id, message)

    new_message = MessageEntry(role=MessageRole.BOT, message="New message")
    adapter.add_message(conversation_id, new_message)

    result = adapter.get_conversation(conversation_id)
    assert len(result) == 2
    assert result[0].message == "Hello!"
    assert result[0].role == MessageRole.USER
    assert result[1].message == "New message"
    assert result[1].role == MessageRole.BOT

def test_add_messages(adapter, conversation_id, messages):
    adapter.add_messages(conversation_id, messages)

    new_message = MessageEntry(role=MessageRole.USER, message="New message")
    other_new_message = MessageEntry(role=MessageRole.BOT, message="Other new message")
    adapter.add_messages(conversation_id, [new_message, other_new_message])

    result = adapter.get_conversation(conversation_id)
    assert len(result) == 4
    assert result[0].message == "Hello!"
    assert result[0].role == MessageRole.USER
    assert result[1].message == "Hi there!"
    assert result[1].role == MessageRole.BOT
    assert result[2].message == "New message"
    assert result[2].role == MessageRole.USER
    assert result[3].message == "Other new message"
    assert result[3].role == MessageRole.BOT

def test_multiple_conversations(adapter):
    conversation_id_1 = "conversation-1"
    conversation_id_2 = "conversation-2"

    adapter.add_message(conversation_id_1, MessageEntry(role=MessageRole.USER, message="Message 1"))
    conversation_1 = adapter.get_conversation(conversation_id_1)

    adapter.add_message(conversation_id_2, MessageEntry(role=MessageRole.USER, message="Message 2"))
    conversation_2 = adapter.get_conversation(conversation_id_2)

    assert conversation_1[0].message == "Message 1"
    assert conversation_2[0].message == "Message 2"
    assert len(conversation_1) == 1
    assert len(conversation_2) == 1

def test_get_conversation_not_exists(adapter):
    result = adapter.get_conversation("test-conversation-invalid")
    assert result is None

def test_add_empty_messages_list(adapter, conversation_id):
    adapter.add_messages(conversation_id, [])

    result = adapter.get_conversation(conversation_id)
    assert result == []

def test_conversation_order(adapter, conversation_id):
    adapter.add_message(conversation_id,MessageEntry(role=MessageRole.USER, message="First"))
    adapter.add_message(conversation_id, MessageEntry(role=MessageRole.BOT, message="Second"))
    adapter.add_messages(conversation_id, [
        MessageEntry(role=MessageRole.USER, message="Third"),
        MessageEntry(role=MessageRole.BOT, message="Fourth")
    ])

    result = adapter.get_conversation(conversation_id)
    assert result[0].message == "First"
    assert result[1].message == "Second"
    assert result[2].message == "Third"
    assert result[3].message == "Fourth"
import pytest
import json
import tempfile
import shutil
from pathlib import Path
from app.models.conversation import MessageEntry, MessageRole
from app.adapters.storage.filesystem import FilesystemStorageAdapter
from app.adapters.storage.base import StorageAdapter

@pytest.fixture
def temp_storage_path():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Cleanup after test
    shutil.rmtree(temp_dir)

@pytest.fixture
def adapter(temp_storage_path):
    return FilesystemStorageAdapter(temp_storage_path)

@pytest.fixture
def conversation_id():
    return "test-conversation-123"

@pytest.fixture
def messages():
    return [
        MessageEntry(role=MessageRole.USER, message="Hello!"),
        MessageEntry(role=MessageRole.BOT, message="Hi there!")
    ]

@pytest.fixture
def message():
    return MessageEntry(role=MessageRole.USER, message="Hello!")

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

    additional_messages = [
        MessageEntry(role=MessageRole.USER, message="New message"),
        MessageEntry(role=MessageRole.BOT, message="Other new message")
    ]
    adapter.add_messages(conversation_id, additional_messages)

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

def test_multiple_conversations(adapter, temp_storage_path):
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

def test_add_empty_messages_list(adapter, conversation_id, temp_storage_path):
    adapter.add_messages(conversation_id, [])

    result = adapter.get_conversation(conversation_id)
    assert result == []

    # Check empty file was created
    file_path = Path(temp_storage_path) / f"{conversation_id}.json"
    assert file_path.exists()


def test_conversation_order(adapter, conversation_id):
    adapter.add_message(conversation_id, MessageEntry(role=MessageRole.USER, message="First"))
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

def test_json_file_format(adapter, conversation_id, messages, temp_storage_path):
    adapter.add_messages(conversation_id, messages)

    file_path = Path(temp_storage_path) / f"{conversation_id}.json"

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    assert len(data) == 2
    assert data[0]["role"] == "user"
    assert data[0]["message"] == "Hello!"
    assert data[1]["role"] == "bot"
    assert data[1]["message"] == "Hi there!"

def test_file_path_generation(adapter):
    conversation_id = "test-conversation-123"
    file_path = adapter._get_file_path(conversation_id)

    assert file_path.name == "test-conversation-123.json"
    assert file_path.suffix == ".json"

def test_storage_directory_creation():
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_path = Path(temp_dir) / "new_conversations"

        # Directory shouldn't exist yet
        assert not storage_path.exists()

        adapter = FilesystemStorageAdapter(str(storage_path))

        assert storage_path.exists()
        assert storage_path.is_dir()

def test_unicode_messages(adapter, conversation_id):
    unicode_messages = [
        MessageEntry(role=MessageRole.USER, message="Hello! 你好 مرحبا"),
        MessageEntry(role=MessageRole.BOT, message="🤖 Émojis and açcénts work!")
    ]

    adapter.add_messages(conversation_id, unicode_messages)

    result = adapter.get_conversation(conversation_id)
    assert result[0].message == "Hello! 你好 مرحبا"
    assert result[1].message == "🤖 Émojis and açcénts work!"
import json
from pathlib import Path
from typing import List, Optional, Dict
from .base import StorageAdapter
from app.models.conversation import MessageEntry

class FilesystemStorageAdapter(StorageAdapter):
    def __init__(self, storage_path: str = "conversations"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def _get_file_path(self, conversation_id: str) -> Path:
        return self.storage_path / f"{conversation_id}.json"

    def _serialize_messages(self, messages: List[MessageEntry]) -> List[Dict]:
        return [
            {
                "role": message.role,
                "message": message.message
            }
            for message in messages
        ]

    def _deserialize_messages(self, data: List[Dict]) -> List[MessageEntry]:
        from app.models.conversation import MessageRole
        return [
            MessageEntry(
                role=item["role"],
                message=item["message"]
            )
            for item in data
        ]

    def _save_conversation(self, conversation_id: str, messages: List[MessageEntry]) -> None:
        file_path = self._get_file_path(conversation_id)

        try:
            data = self._serialize_messages(messages)

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        except (IOError, OSError) as e:
            print(f"Error saving conversation {conversation_id}: {e}")
            raise

    def get_conversation(self, conversation_id: str) -> Optional[List[MessageEntry]]:
        file_path = self._get_file_path(conversation_id)

        if not file_path.exists():
            return None

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return self._deserialize_messages(data)
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error reading conversation {conversation_id}: {e}")
            return None

    def add_message(self, conversation_id: str, message: MessageEntry) -> None:
        messages = self.get_conversation(conversation_id) or []        
        messages.append(message)
        self._save_conversation(conversation_id, messages)

    def add_messages(self, conversation_id: str, messages: List[MessageEntry]) -> None:
        existing_messages = self.get_conversation(conversation_id) or []
        existing_messages.extend(messages)
        self._save_conversation(conversation_id, existing_messages)

    def delete_conversation(self, conversation_id: str) -> None:
        file_path = self._get_file_path(conversation_id)

        if file_path.exists():
            try:
                file_path.unlink()
            except (IOError, OSError) as e:
                print(f"Error deleting conversation {conversation_id}: {e}")
                raise

    def conversation_exists(self, conversation_id: str) -> bool:
        file_path = self._get_file_path(conversation_id)
        return file_path.exists()
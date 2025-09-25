from uuid import uuid4
from fastapi import APIRouter
from app.models.conversation import ConversationRequest, ConversationResponse, MessageRole, MessageEntry
from app.adapters.storage.memory import MemoryStorageAdapter

router = APIRouter(prefix="/v1", tags=["conversation"])

storage_adapter = MemoryStorageAdapter()

@router.post("/conversation", response_model=ConversationResponse)
def conversation_endpoint(req: ConversationRequest):
    conversation_id = req.conversation_id or str(uuid4())
    user_message = MessageEntry(role=MessageRole.USER, message=req.message)
    bot_message = MessageEntry(role=MessageRole.BOT, message="Hi! I'm your chatbot.")

    storage_adapter.add_messages(conversation_id, [user_message, bot_message])
    messages = storage_adapter.get_conversation(conversation_id) or []

    return ConversationResponse(
        conversation_id = conversation_id,
        message = messages
    )
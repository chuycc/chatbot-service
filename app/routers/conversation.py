from uuid import uuid4
from fastapi import APIRouter
from app.models.conversation import ConversationRequest, ConversationResponse, MessageRole, MessageEntry

router = APIRouter(prefix="/v1", tags=["conversation"])

@router.post("/conversation", response_model=ConversationResponse)
def conversation_endpoint(req: ConversationRequest):
    conv_id = req.conversation_id or str(uuid4())
    user_message = MessageEntry(role=MessageRole.USER, message=req.message)
    bot_message = MessageEntry(role=MessageRole.BOT, message="Hi! I'm your chatbot.")
    return ConversationResponse(
        conversation_id=conv_id,
        message=[user_message, bot_message]
    )
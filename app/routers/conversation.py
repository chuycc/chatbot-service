from uuid import uuid4
import asyncio
from fastapi import APIRouter, HTTPException, Request
from app.models.conversation import ConversationRequest, ConversationResponse, MessageRole, MessageEntry
from app.adapters.storage import get_storage_adapter
from app.adapters.llm import get_llm_adapter
from app.config import settings
from app.middleware.rate_limit import limiter

router = APIRouter(prefix="/v1", tags=["conversation"])

storage_adapter = get_storage_adapter()
llm_adapter = get_llm_adapter()

@router.post("/conversation", response_model=ConversationResponse)
@limiter.limit(settings.service_rate_limit)
async def conversation_endpoint(req: ConversationRequest, request: Request):
    if req.conversation_id is not None and not storage_adapter.conversation_exists(req.conversation_id):
        raise HTTPException(
            status_code=404,
            detail=f"I can't find a conversation with id '{req.conversation_id}'."
        )

    conversation_id = req.conversation_id or str(uuid4())

    # User message
    user_message = MessageEntry(role=MessageRole.USER, message=req.message)
    storage_adapter.add_message(conversation_id, user_message)

    # Bot message
    conversation_messages = storage_adapter.get_conversation(conversation_id)

    try:
        bot_response = await llm_adapter.send_chat_messages(conversation_messages)
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail="I apologize, but the response took too long. Please try again."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="I apologize, but I'm having trouble generating a response right now. Please try again later."
        )

    bot_message = MessageEntry(role=MessageRole.BOT, message=bot_response)
    storage_adapter.add_message(conversation_id, bot_message)

    messages = storage_adapter.get_conversation(conversation_id)

    return ConversationResponse(
        conversation_id = conversation_id,
        message = messages
    )
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    BOT = "bot"

class MessageEntry(BaseModel):
    role: MessageRole
    message: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="The message content"
    )
    
    class Config:
        use_enum_values = True
        schema_extra = {
            "example": {
                "role": "user",
                "message": "Hello!"
            }
        }

class ConversationRequest(BaseModel):
    conversation_id: Optional[str] = Field(
        None,
        description="Existing conversation ID or null for new conversation"
    )
    message: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="User message"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
                "message": "Hello!"
            }
        }

class ConversationResponse(BaseModel):
    conversation_id: str = Field(
        ...,
        description="The conversation identifier")
    message: List[MessageEntry] = Field(
        ...,
        description="List of messages in the conversation")
    
    class Config:
        schema_extra = {
            "example": {
                "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
                "message": [
                    {
                        "role": "user",
                        "message": "Hello!"
                    },
                    {
                        "role": "bot", 
                        "message": "Hi!"
                    }
                ]
            }
        }
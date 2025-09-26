import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_conversation_endpoint_new_conversation(monkeypatch):
    # Remove system prompt to ensure consistent test results
    from app.routers import conversation
    monkeypatch.setattr(conversation.llm_adapter, "_load_system_prompt", lambda self=None: None)

    payload = {
        "conversation_id": None,
        "message": "2 + 2? Only give the number"
    }
    
    response = client.post("/v1/conversation", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    # Check response structure
    assert "conversation_id" in data
    assert "message" in data
    assert isinstance(data["message"], list)
    assert len(data["message"]) == 2
    
    # Check message content
    assert data["message"][0]["role"] == "user"
    assert data["message"][0]["message"] == "2 + 2? Only give the number"
    assert data["message"][1]["role"] == "bot"
    assert data["message"][1]["message"] == "4"
    
    # Check conversation_id is generated
    assert data["conversation_id"] is not None
    assert len(data["conversation_id"]) > 0


def test_conversation_endpoint_existing_conversation():
    # Step 1: Start a new conversation
    payload1 = {
        "conversation_id": None,
        "message": "Hello!"
    }
    response1 = client.post("/v1/conversation", json=payload1)
    assert response1.status_code == 200
    data1 = response1.json()
    conversation_id = data1["conversation_id"]
    assert conversation_id is not None

    # Step 2: Send another message using the returned conversation_id
    payload2 = {
        "conversation_id": conversation_id,
        "message": "Hello again!"
    }
    response2 = client.post("/v1/conversation", json=payload2)
    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["conversation_id"] == conversation_id
    assert len(data2["message"]) == 4
    assert data2["message"][0]["role"] == "user"
    assert data2["message"][1]["role"] == "bot"
    assert data2["message"][2]["role"] == "user"
    assert data2["message"][3]["role"] == "bot"

def test_conversation_endpoint_empty_message():
    payload = {
        "conversation_id": None,
        "message": ""
    }
    
    response = client.post("/v1/conversation", json=payload)
    
    assert response.status_code == 422

def test_conversation_endpoint_long_message():
    payload = {
        "conversation_id": None,
        "message": "x" * 1001
    }
    
    response = client.post("/v1/conversation", json=payload)
    
    assert response.status_code == 422

def test_conversation_endpoint_missing_message():
    payload = {
        "conversation_id": None
        # message field missing
    }
    
    response = client.post("/v1/conversation", json=payload)
    
    assert response.status_code == 422

def test_conversation_endpoint_invalid_json():
    response = client.post(
        "/v1/conversation",
        data="invalid json",
        headers={"Content-Type": "application/json"}
    )
    
    assert response.status_code == 422

def test_conversation_endpoint_timeout_handling(monkeypatch):
    from app.routers import conversation

    async def mock_send_chat_messages_timeout(*args, **kwargs):
        import asyncio
        raise asyncio.TimeoutError()

    monkeypatch.setattr(conversation.llm_adapter, "send_chat_messages", mock_send_chat_messages_timeout)

    payload = {
        "conversation_id": None,
        "message": "Timeout?"
    }

    response = client.post("/v1/conversation", json=payload)
    assert response.status_code == 504
    assert "response took too long" in response.json()["detail"]

def test_conversation_endpoint_llm_error_handling(monkeypatch):
    from app.routers import conversation

    async def mock_send_chat_messages_error(*args, **kwargs):
        raise Exception("LLM error")

    monkeypatch.setattr(conversation.llm_adapter, "send_chat_messages", mock_send_chat_messages_error)

    payload = {
        "conversation_id": None,
        "message": "Trigger LLM error"
    }

    response = client.post("/v1/conversation", json=payload)
    assert response.status_code == 500
    assert "trouble generating a response" in response.json()["detail"]

def test_conversation_endpoint_invalid_conversation_id():
    payload = {
        "conversation_id": "invalid-id-123",
        "message": "Hi!"
    }
    response = client.post("/v1/conversation", json=payload)
    assert response.status_code == 404
    assert "invalid-id-123" in response.json()["detail"]
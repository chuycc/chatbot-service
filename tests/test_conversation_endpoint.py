import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_conversation_endpoint_new_conversation():
    payload = {
        "conversation_id": None,
        "message": "Hello, bot!"
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
    assert data["message"][0]["message"] == "Hello, bot!"
    assert data["message"][1]["role"] == "bot"
    assert data["message"][1]["message"] == "Hi! I'm your chatbot."
    
    # Check conversation_id is generated
    assert data["conversation_id"] is not None
    assert len(data["conversation_id"]) > 0

def test_conversation_endpoint_existing_conversation():
    payload = {
        "conversation_id": "test-conversation-123",
        "message": "How are you?"
    }
    
    response = client.post("/v1/conversation", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["conversation_id"] == "test-conversation-123"

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
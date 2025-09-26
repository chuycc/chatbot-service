# chatbot-service
Chatbot service built with FastAPI and powered by Large Language Models. Containerized with Docker for easy deployment and scalability.

## TODO
- [X] Create Dockerfile
- [ ] Create Makefile
    - [X] make install
    - [X] make run
    - [X] make down
    - [X] make clean
    - [ ] make test
    - [X] make
- [ ] Chatbot API
    - [X] Data Models
    - [X] Basic endpoint
    - [X] Storage adapter
    - [X] LLM layer
    - [ ] Conversation manager

## Environment variables
Environment variables can be configured in a `.env` file or set directly in your shell environment.

These variables allow you to configure the chatbot service without modifying the codebase. Below are the supported options:
```
SERVICE_TIMEOUT=30
STORAGE_TYPE=memory (Default) | filesystem
FILESYSTEM_STORAGE_PATH=conversations
LLM_TYPE=openai
LLM_TIMEOUT=30
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_CHAT_SETTINGS={"model": "gpt-4o", "max_completion_tokens": 1000, "temperature": 0.5, "OTHER_PARAM": "value"}
```

## Adapters
This service is designed with a flexible adapter architecture, allowing support for multiple Storage types and LLMs.
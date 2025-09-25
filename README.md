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
    - [ ] LLM layer
    - [ ] Conversation manager

## Storage adapter
The service is designed with a flexible storage adapter architecture, allowing support for multiple storage backends such as memory, filesystem, Redis, databases, and more.

Currently, `memory` is the default and only supported storage type. Additional adapters (e.g., Redis, database, filesystem) can be added as needed.

You can configure the storage type in multiple ways:
### 1. `.env` file
`STORAGE_TYPE=memory`

### 2. Environment variable
`STORAGE_TYPE=memory uvicorn app.main:app --reload`
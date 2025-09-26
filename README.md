# chatbot-service
Chatbot service built with FastAPI and powered by Large Language Models. Containerized with Docker for easy deployment and scalability.

## TODO
- [X] Create Dockerfile
- [X] Create Makefile
    - [X] make install
    - [X] make run
    - [X] make down
    - [X] make clean
    - [X] make test
    - [X] make
- [X] Chatbot API
    - [X] Data Models
    - [X] Basic endpoint
    - [X] Storage adapter
    - [X] LLM adapter

## Usage
make commands

```
install  - Install all requirements to run the service
run      - Run the service and all related services in Docker
down     - Teardown of all running services
clean    - Teardown and removal of all containers
test     - Run tests
```

Example
```
$ make run
Stopping Docker container...
Removing Docker container...
Removing Docker image...
Building Docker image...
Running Docker container...

$ curl -X POST http://127.0.0.1:8000/v1/conversation -H "Content-Type: application/json" -d '{"message": "2 + 2"}'

{"conversation_id":"cc20fc6d-6546-44fa-a08a-2c160e0115be","message":[{"role":"user","message":"2 + 2 equals 4."}]}

$ curl -X POST http://127.0.0.1:8000/v1/conversation -H "Content-Type: application/json" -d '{"conversation_id":"cc20fc6d-6546-44fa-a08a-2c160e0115be", "message": "*5"}'

{"conversation_id":"cc20fc6d-6546-44fa-a08a-2c160e0115be","message":[{"role":"user","message":"2 + 2"},{"role":"bot","message":"2 + 2 equals 4."},{"role":"user","message":"*5"},{"role":"bot","message":"4 * 5 equals 20."}]}
```

## Endpoint
POST ```/v1/conversation```

Content-Type: application/json

### Request
```
{
    "conversation_id": "text" | null,
    "message": "text"
}
```

### Response
```
{
    "conversation_id": "text",
     "message": [
        {
            "role": "user",
            "message": "text"
        },
        {
            "role": "bot",
            "message": "text"
        }
    ]
}
```

## Environment variables
Environment variables can be configured in a `.env` file or set directly in your shell environment.

These are the supported environment variables:
```
SERVICE_TIMEOUT=30
STORAGE_TYPE=memory | filesystem # default: memory
FILESYSTEM_STORAGE_PATH=conversations
LLM_TYPE=openai
LLM_TIMEOUT=30
LLM_SYSTEM_PROMPT_PATH=app/prompts/system_prompt.txt
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_CHAT_SETTINGS={"model": "gpt-4o", "max_completion_tokens": 1000, "temperature": 0.5, "OTHER_PARAM": "value"}
```

## LLM system prompt
The "system" role is used to provide high-level instructions and context to the language model. It acts as a set of guidelines that influence the model's overall behavior and response generation.

The system prompt can be defined in `prompts/systemt_prompt.txt`

## Adapters
This service is designed with a flexible adapter architecture, allowing support for multiple Storage types and LLMs.

## Future work
* Auth middleware
* Rate middleware
* Error handling
* Logs handling
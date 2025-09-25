from fastapi import FastAPI
from app.routers import conversation

app = FastAPI()
app.include_router(conversation.router)

@app.get("/")
def read_root():
    return {"message": "Chatbot Service is running"}

@app.get("/health")
def health():
    return {"message": "Healthy"}

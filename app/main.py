from fastapi import FastAPI
from app.middleware.timeout import TimeoutMiddleware
from app.routers import conversation
from app.config import settings

app = FastAPI()
app.add_middleware(TimeoutMiddleware, settings.service_timeout)
app.include_router(conversation.router)

@app.get("/")
def read_root():
    return {"message": "Chatbot Service is running"}

@app.get("/health")
def health():
    return {"message": "Healthy"}

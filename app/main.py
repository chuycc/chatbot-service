from fastapi import FastAPI
from app.middleware.timeout import TimeoutMiddleware
from app.routers import conversation
from app.config import settings
from slowapi.errors import RateLimitExceeded
from app.middleware.rate_limit import limiter, rate_limit_exceeded_handler

app = FastAPI()
app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
app.add_middleware(TimeoutMiddleware, timeout=settings.service_timeout)
app.include_router(conversation.router)

@app.get("/")
def read_root():
    return {"message": "Chatbot Service is running"}

@app.get("/health")
def health():
    return {"message": "Healthy"}

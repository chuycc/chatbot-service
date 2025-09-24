from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Chatbot Service is running"}

@app.get("/health")
def health():
    return {"message": "Healthy"}

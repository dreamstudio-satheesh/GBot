# main.py - FastAPI Entry Point

from fastapi import FastAPI
from app.routes import auth
from app.database import engine, Base

# Initialize Database
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(title="AI Chatbot API", version="1.0")

# Include authentication routes
app.include_router(auth.router)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Chatbot API"}






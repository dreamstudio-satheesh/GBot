from fastapi import FastAPI
from app.auth import auth_router
from app.database import Base, engine

# Initialize DB
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Chatbot API")

# Include authentication routes
app.include_router(auth_router)

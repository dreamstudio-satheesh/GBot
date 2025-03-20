from fastapi import FastAPI
from app.routes.chatbot import router as chatbot_router
from app.routes.knowledge_base import router as knowledge_router
from app.routes.vector_search import router as vector_router
from app.routes.admin import router as admin_router
from app.routes.system_monitoring import router as monitoring_router

app = FastAPI()

# Register API Routes
app.include_router(chatbot_router, prefix="/chatbot", tags=["Chatbot"])
app.include_router(knowledge_router, prefix="/knowledge-base", tags=["Knowledge Base"])
app.include_router(vector_router, prefix="/vector-search", tags=["Vector Search"])
app.include_router(logs_router, prefix="/logs", tags=["Logs"])
app.include_router(monitoring_router, prefix="/system", tags=["System Monitoring"])

@app.get("/")
def root():
    return {"message": "AI Chatbot API is running!"}

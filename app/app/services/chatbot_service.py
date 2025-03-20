from sqlalchemy.orm import Session
from app.models import KnowledgeBase, ChatLogs, ChatbotSettings
from app.services.vector_service import search_vector_entries
import requests
import os
import time
from datetime import datetime, timedelta
from cachetools import TTLCache

# Load OpenRouter API Key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/generate"

# Caching Mechanism (Cache AI responses for 10 minutes, max 100 queries)
cached_responses = TTLCache(maxsize=100, ttl=600)

# Rate Limit Dictionary (Allow max 5 AI queries per user per minute)
user_rate_limits = {}
RATE_LIMIT = 5  # Max AI calls per minute

def handle_chat_query(db: Session, message: str, user_id: int):
    """Handles chatbot queries with RAG, caching, and rate limiting."""
    global user_rate_limits
    
    # Step 1: Check Knowledge Base for direct match
    db_entry = db.query(KnowledgeBase).filter(KnowledgeBase.content.ilike(f"%{message}%")).first()
    if db_entry:
        log_chat_interaction(db, user_id, message, db_entry.content, "knowledge_base")
        return db_entry.content
    
    # Step 2: Use Vector Search to find similar responses
    vector_results = search_vector_entries(db, message)
    if vector_results:
        best_match = vector_results[0]  # Take the most relevant response
        knowledge_entry = db.query(KnowledgeBase).filter(KnowledgeBase.id == best_match["knowledge_id"]).first()
        if knowledge_entry:
            log_chat_interaction(db, user_id, message, knowledge_entry.content, "vector_search")
            return knowledge_entry.content
    
    # Step 3: Check Cache for AI Response
    if message in cached_responses:
        cached_response = cached_responses[message]
        log_chat_interaction(db, user_id, message, cached_response, "cached_ai_response")
        return cached_response
    
    # Step 4: Apply Rate Limit per User
    current_time = time.time()
    user_requests = user_rate_limits.get(user_id, [])
    user_requests = [t for t in user_requests if current_time - t < 60]  # Keep only last 60 seconds requests
    
    if len(user_requests) >= RATE_LIMIT:
        return "Rate limit exceeded. Please wait before making another AI request."
    
    user_requests.append(current_time)
    user_rate_limits[user_id] = user_requests
    
    # Step 5: If no match found, use OpenRouter AI Model
    ai_response = generate_ai_response(message)
    cached_responses[message] = ai_response  # Store in cache
    log_chat_interaction(db, user_id, message, ai_response, "ai_model")
    return ai_response

def generate_ai_response(message: str) -> str:
    """Generates a chatbot response using OpenRouter API."""
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    data = {"prompt": message, "max_tokens": 150}
    response = requests.post(OPENROUTER_API_URL, json=data, headers=headers)
    if response.status_code == 200:
        return response.json().get("text", "I couldn't generate a response.")
    return "AI service is currently unavailable."

def log_chat_interaction(db: Session, user_id: int, message: str, response: str, source: str):
    """Logs chatbot interactions for future analysis."""
    chat_log = ChatLogs(
        user_id=user_id,
        message=message,
        response=response,
        source=source,
        created_at=datetime.utcnow()
    )
    db.add(chat_log)
    db.commit()

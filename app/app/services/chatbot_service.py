from sqlalchemy.orm import Session
from app.models import KnowledgeBase, ChatLogs, ChatbotSettings
from app.services.vector_service import search_vector_entries
from app.services.ai_service import generate_ai_response  # AI model integration
from datetime import datetime

def handle_chat_query(db: Session, message: str):
    """Handles chatbot queries by searching knowledge base, vector search, and AI model fallback."""
    
    # Step 1: Check Knowledge Base for direct match
    db_entry = db.query(KnowledgeBase).filter(KnowledgeBase.content.ilike(f"%{message}%")).first()
    if db_entry:
        log_chat_interaction(db, message, db_entry.content, "knowledge_base")
        return db_entry.content
    
    # Step 2: Use Vector Search to find similar responses
    vector_results = search_vector_entries(db, message)
    if vector_results:
        best_match = vector_results[0]  # Take the most relevant response
        knowledge_entry = db.query(KnowledgeBase).filter(KnowledgeBase.id == best_match["knowledge_id"]).first()
        if knowledge_entry:
            log_chat_interaction(db, message, knowledge_entry.content, "vector_search")
            return knowledge_entry.content
    
    # Step 3: If no match found, use AI Model as fallback
    ai_response = generate_ai_response(message)
    log_chat_interaction(db, message, ai_response, "ai_model")
    return ai_response

def log_chat_interaction(db: Session, message: str, response: str, source: str):
    """Logs chatbot interactions for future analysis."""
    chat_log = ChatLogs(
        message=message,
        response=response,
        source=source,
        created_at=datetime.utcnow()
    )
    db.add(chat_log)
    db.commit()

def get_chat_history(db: Session, user_id: int):
    """Retrieves past chatbot interactions for a user."""
    return db.query(ChatLogs).filter(ChatLogs.user_id == user_id).order_by(ChatLogs.created_at.desc()).all()

def get_chatbot_settings(db: Session):
    """Retrieves chatbot settings from the database."""
    return db.query(ChatbotSettings).all()

def update_chatbot_settings(db: Session, setting_key: str, setting_value: str):
    """Updates chatbot settings dynamically."""
    setting = db.query(ChatbotSettings).filter(ChatbotSettings.setting_key == setting_key).first()
    if setting:
        setting.setting_value = setting_value
        db.commit()
        return True
    return False

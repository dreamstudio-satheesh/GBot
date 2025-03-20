from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.chatbot_service import handle_chat_query, get_chat_history, get_chatbot_settings, update_chatbot_settings
from app.services.auth_service import get_current_user

router = APIRouter()

class ChatQuery(BaseModel):
    message: str

class ChatbotSettingsUpdate(BaseModel):
    setting_key: str
    setting_value: str

@router.post("/chatbot/query")
def chatbot_query(query: ChatQuery, db: Session = Depends(get_db)):
    """Process user query and fetch chatbot response."""
    response = handle_chat_query(db, query.message)
    if not response:
        raise HTTPException(status_code=404, detail="No suitable response found")
    return {"response": response}

@router.get("/chatbot/history")
def chatbot_history(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """Retrieve past chatbot interactions."""
    history = get_chat_history(db, user["id"])
    return history

@router.get("/chatbot/settings")
def chatbot_settings(db: Session = Depends(get_db)):
    """Get chatbot settings."""
    return get_chatbot_settings(db)

@router.put("/chatbot/settings/update")
def update_settings(update_data: ChatbotSettingsUpdate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """Update chatbot settings."""
    success = update_chatbot_settings(db, update_data.setting_key, update_data.setting_value)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update settings")
    return {"message": "Settings updated successfully"}

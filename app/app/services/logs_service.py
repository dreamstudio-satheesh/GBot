from sqlalchemy.orm import Session
from app.models import ChatLogs

def get_all_logs(db: Session, user_id: int):
    """Retrieves all chat logs for a specific user."""
    return db.query(ChatLogs).filter(ChatLogs.user_id == user_id).order_by(ChatLogs.created_at.desc()).all()

def get_log_by_id(db: Session, log_id: int, user_id: int):
    """Retrieves a specific chat log entry by ID."""
    return db.query(ChatLogs).filter(ChatLogs.id == log_id, ChatLogs.user_id == user_id).first()

def delete_log_entry(db: Session, log_id: int, user_id: int):
    """Deletes a chat log entry if it belongs to the user."""
    log_entry = db.query(ChatLogs).filter(ChatLogs.id == log_id, ChatLogs.user_id == user_id).first()
    if not log_entry:
        return False
    db.delete(log_entry)
    db.commit()
    return True
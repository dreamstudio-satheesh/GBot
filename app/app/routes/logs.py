from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.logs_service import get_all_logs, get_log_by_id, delete_log_entry

router = APIRouter()

@router.get("/logs/conversations")
def get_chat_logs(db: Session = Depends(get_db)):
    """Retrieve all chatbot conversation logs."""
    logs = get_all_logs(db, user["id"])
    return logs

@router.get("/logs/conversations/{id}")
def get_chat_log(id: int, db: Session = Depends(get_db)):
    """Retrieve a specific chatbot conversation log."""
    log_entry = get_log_by_id(db, id, user["id"])
    if not log_entry:
        raise HTTPException(status_code=404, detail="Chat log not found")
    return log_entry

@router.delete("/logs/delete/{id}")
def delete_chat_log(id: int, db: Session = Depends(get_db)):
    """Delete a conversation log."""
    success = delete_log_entry(db, id, user["id"])
    if not success:
        raise HTTPException(status_code=404, detail="Chat log not found or not authorized to delete")
    return {"message": "Chat log deleted successfully"}

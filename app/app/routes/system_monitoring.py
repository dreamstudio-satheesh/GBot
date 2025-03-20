import psutil
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.system_monitoring_service import get_api_usage_stats, get_system_logs
router = APIRouter()

def admin_only(user: dict):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

@router.get("/system/health")
def system_health():
    """Check system health status."""
    return {"status": "ok", "cpu_usage": psutil.cpu_percent(), "memory_usage": psutil.virtual_memory().percent}

@router.get("/system/stats")
def system_stats(db: Session = Depends(get_db)):
    """Get API usage and performance stats (Admin only)."""
    admin_only(user)
    return get_api_usage_stats(db)

@router.get("/system/logs")
def system_logs():
    """Fetch system logs (Admin only)."""
    admin_only(user)
    return get_system_logs()

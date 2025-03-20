import psutil
import os
from sqlalchemy.orm import Session
from app.models import APIKey

def get_api_usage_stats(db: Session):
    """Retrieve API usage statistics from the database."""
    total_api_keys = db.query(APIKey).count()
    return {
        "total_api_keys": total_api_keys,
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage("/").percent
    }

def get_system_logs():
    """Fetch system logs from the server."""
    log_file_path = "/var/log/syslog" if os.path.exists("/var/log/syslog") else "/var/log/system.log"
    try:
        with open(log_file_path, "r") as log_file:
            logs = log_file.readlines()[-50:]  # Get the last 50 log lines
        return {"logs": logs}
    except Exception as e:
        return {"error": str(e)}
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.admin_service import get_all_users, update_user, delete_user, get_all_tenants, create_tenant
from app.services.auth_service import get_current_user

router = APIRouter()

def admin_only(user: dict):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

@router.get("/admin/users")
def list_users(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """List all users (Admin only)."""
    admin_only(user)
    return get_all_users(db)

@router.put("/admin/users/update/{id}")
def modify_user(id: int, update_data: dict, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """Update user details (Admin only)."""
    admin_only(user)
    success = update_user(db, id, update_data)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated successfully"}

@router.delete("/admin/users/delete/{id}")
def remove_user(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """Delete a user (Admin only)."""
    admin_only(user)
    success = delete_user(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@router.get("/admin/tenants")
def list_tenants(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """List all tenants (Admin only)."""
    admin_only(user)
    return get_all_tenants(db)

@router.post("/admin/tenants/create")
def new_tenant(tenant_data: dict, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """Create a new tenant (Admin only)."""
    admin_only(user)
    return create_tenant(db, tenant_data)

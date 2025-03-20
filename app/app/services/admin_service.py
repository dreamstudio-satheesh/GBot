from sqlalchemy.orm import Session
from app.models import User, Tenant

def get_all_users(db: Session):
    """Retrieves all users from the database."""
    return db.query(User).all()

def update_user(db: Session, user_id: int, update_data: dict):
    """Updates user details."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    return True

def delete_user(db: Session, user_id: int):
    """Deletes a user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True

def get_all_tenants(db: Session):
    """Retrieves all tenants from the database."""
    return db.query(Tenant).all()

def create_tenant(db: Session, tenant_data: dict):
    """Creates a new tenant."""
    new_tenant = Tenant(**tenant_data)
    db.add(new_tenant)
    db.commit()
    db.refresh(new_tenant)
    return new_tenant
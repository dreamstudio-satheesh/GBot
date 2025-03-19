from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..services import auth_service
import uuid

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = auth_service.get_password_hash(user.password)
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=schemas.TokenResponse)
def login(user: schemas.LoginRequest, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not auth_service.verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = auth_service.create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout():
    return {"message": "Logged out successfully"}

@router.get("/me", response_model=schemas.UserResponse)
def get_current_user(db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == 1).first()  # Replace with real user fetching logic
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/api-key/generate", response_model=schemas.APIKeyResponse)
def generate_api_key(db: Session = Depends(get_db)):
    api_key = str(uuid.uuid4())
    new_api_key = models.APIKey(user_id=1, api_key=api_key)  # Replace with real user fetching logic
    db.add(new_api_key)
    db.commit()
    db.refresh(new_api_key)
    return new_api_key

@router.get("/api-key/list", response_model=list[schemas.APIKeyResponse])
def list_api_keys(db: Session = Depends(get_db)):
    return db.query(models.APIKey).filter(models.APIKey.user_id == 1).all()  # Replace with real user fetching logic

@router.delete("/api-key/revoke/{key_id}")
def revoke_api_key(key_id: int, db: Session = Depends(get_db)):
    api_key = db.query(models.APIKey).filter(models.APIKey.id == key_id, models.APIKey.user_id == 1).first()
    if not api_key:
        raise HTTPException(status_code=404, detail="API Key not found")
    db.delete(api_key)
    db.commit()
    return {"message": "API key revoked"}

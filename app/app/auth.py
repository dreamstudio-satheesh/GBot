from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, Token
from app.services.auth_service import create_access_token, verify_password, hash_password, get_current_user

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@auth_router.post("/register", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """ Register a new user """
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user_data.password)
    new_user = User(username=user_data.username, email=user_data.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate JWT Token
    access_token = create_access_token(data={"sub": new_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """ Authenticate user and return JWT token """
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/api-key")
def generate_api_key(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """ Generate a unique API key for the user """
    import secrets
    api_key = secrets.token_hex(32)

    current_user.api_key = api_key
    db.commit()
    db.refresh(current_user)

    return {"api_key": api_key}


@auth_router.get("/me")
def get_user_details(current_user: User = Depends(get_current_user)):
    """ Get details of the currently logged-in user """
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "api_key": current_user.api_key
    }

from datetime import datetime, timedelta
from typing import Any, Union, Optional
from jose import jwt, JWTError
from fastapi import HTTPException, status
from .config import settings
import uuid
import hashlib

# Using werkzeug for password hashing instead of bcrypt due to compatibility issues

def create_access_token(
    subject: Union[str, Any], 
    tenant_id: str,
    user_role: str,
    expires_delta: timedelta = None
) -> str:
    """Create JWT access token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "tenant_id": tenant_id,
        "user_role": user_role,
        "token_type": "access"
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(
    subject: Union[str, Any],
    tenant_id: str,
    expires_delta: timedelta = None
) -> str:
    """Create JWT refresh token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "tenant_id": tenant_id,
        "token_type": "refresh",
        "jti": str(uuid.uuid4())  # JWT ID for refresh token rotation
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

import hashlib

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return hashlib.sha256(password.encode()).hexdigest()

def decode_token(token: str) -> dict:
    """Decode and verify JWT token"""
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Dependency function for FastAPI
from fastapi import Depends
from fastapi.security import HTTPBearer
from ..models.user import User

security = HTTPBearer()

async def get_current_user(credentials = Depends(security)):
    """Get current authenticated user"""
    from .middleware import get_current_user_and_tenant
    from .database import get_database
    
    try:
        # Get user info from token
        user_info = await get_current_user_and_tenant(credentials)
        
        # Get full user details from database
        db = await get_database()
        users_collection = db.get_default_database().users
        user_doc = await users_collection.find_one({
            "_id": user_info["user_id"],
            "tenant_id": user_info["tenant_id"]
        })
        
        if not user_doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Create a simple namespace object to allow dot notation access
        class UserNamespace:
            def __init__(self, data):
                for key, value in data.items():
                    setattr(self, key, value)
        
        return UserNamespace(user_doc)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
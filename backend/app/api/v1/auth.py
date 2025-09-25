from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from datetime import timedelta
from typing import Dict, Any
from ...core.database import get_database
from ...core.security import (
    verify_password, 
    get_password_hash, 
    create_access_token, 
    create_refresh_token,
    decode_token
)
from ...core.config import settings
from ...core.middleware import get_tenant_from_code
from ...models.user import UserLogin, UserCreate, TokenResponse, UserResponse, UserRole, UserStatus
from ...models.tenant import TenantCreate, TenantResponse, TenantStatus
import uuid
from datetime import datetime

router = APIRouter()
security = HTTPBearer()

@router.post("/auth/register-tenant", response_model=Dict[str, Any])
async def register_tenant_and_admin(tenant_data: TenantCreate):
    """Register a new tenant and create admin user"""
    db = await get_database()
    tenants_collection = db.get_default_database().tenants
    users_collection = db.get_default_database().users
    
    # Check if tenant code or domain already exists
    existing_tenant = await tenants_collection.find_one({
        "$or": [
            {"code": tenant_data.code},
            {"domain": tenant_data.domain}
        ]
    })
    
    if existing_tenant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant code or domain already exists"
        )
    
    # Create tenant
    tenant_id = str(uuid.uuid4())
    tenant_doc = {
        "_id": tenant_id,
        "name": tenant_data.name,
        "code": tenant_data.code,
        "domain": tenant_data.domain,
        "status": TenantStatus.TRIAL,
        "plan": tenant_data.plan,
        "admin_email": tenant_data.admin_email,
        "admin_name": tenant_data.admin_name,
        "phone": tenant_data.phone,
        "max_users": 10,
        "max_projects": 50,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    # Create admin user
    admin_user_id = str(uuid.uuid4())
    admin_username = f"admin_{tenant_data.code}"
    default_password = "Welcome123!"  # Force change on first login
    
    admin_user_doc = {
        "_id": admin_user_id,
        "tenant_id": tenant_id,
        "username": admin_username,
        "email": tenant_data.admin_email,
        "full_name": tenant_data.admin_name,
        "hashed_password": get_password_hash(default_password),
        "role": UserRole.ADMIN,
        "status": UserStatus.ACTIVE,
        "permissions": [],
        "portfolio_access": [],
        "project_access": [],
        "preferences": {},
        "failed_login_attempts": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "created_by": admin_user_id,
        "is_active": True,
        "metadata": {}
    }
    
    # Insert both documents
    await tenants_collection.insert_one(tenant_doc)
    await users_collection.insert_one(admin_user_doc)
    
    return {
        "message": "Tenant and admin user created successfully",
        "tenant_id": tenant_id,
        "tenant_code": tenant_data.code,
        "admin_username": admin_username,
        "temporary_password": default_password,
        "login_url": f"/api/v1/auth/login"
    }

@router.post("/auth/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """Authenticate user and return access tokens"""
    db = await get_database()
    
    # Get tenant information
    tenant = await get_tenant_from_code(credentials.tenant_code)
    tenant_id = tenant["_id"]
    
    # Find user by username and tenant
    users_collection = db.get_default_database().users
    user = await users_collection.find_one({
        "username": credentials.username,
        "tenant_id": tenant_id,
        "is_active": True
    })
    
    if not user or not verify_password(credentials.password, user["hashed_password"]):
        # Increment failed login attempts
        if user:
            await users_collection.update_one(
                {"_id": user["_id"]},
                {"$inc": {"failed_login_attempts": 1}}
            )
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username, password, or tenant code",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is suspended or inactive
    if user["status"] != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User account is {user['status']}"
        )
    
    # Reset failed login attempts and update last login
    await users_collection.update_one(
        {"_id": user["_id"]},
        {
            "$set": {
                "failed_login_attempts": 0,
                "last_login": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    # Create tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user["_id"],
        tenant_id=tenant_id,
        user_role=user["role"],
        expires_delta=access_token_expires
    )
    
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_refresh_token(
        subject=user["_id"],
        tenant_id=tenant_id,
        expires_delta=refresh_token_expires
    )
    
    # Create user response
    user_response = UserResponse(
        id=user["_id"],
        username=user["username"],
        email=user["email"],
        full_name=user["full_name"],
        role=user["role"],
        status=user["status"],
        job_title=user.get("job_title"),
        department=user.get("department"),
        phone=user.get("phone"),
        avatar_url=user.get("avatar_url"),
        last_login=user.get("last_login"),
        created_at=user["created_at"],
        updated_at=user["updated_at"]
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=user_response
    )

@router.post("/auth/refresh", response_model=Dict[str, Any])
async def refresh_token(refresh_token: str):
    """Refresh access token using refresh token"""
    try:
        payload = decode_token(refresh_token)
        
        if payload.get("token_type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        user_id = payload.get("sub")
        tenant_id = payload.get("tenant_id")
        
        # Verify user still exists and is active
        db = await get_database()
        users_collection = db.get_default_database().users
        user = await users_collection.find_one({
            "_id": user_id,
            "tenant_id": tenant_id,
            "is_active": True,
            "status": UserStatus.ACTIVE
        })
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # Create new access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = create_access_token(
            subject=user_id,
            tenant_id=tenant_id,
            user_role=user["role"],
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )

@router.post("/auth/logout")
async def logout():
    """Logout user (client should discard tokens)"""
    return {"message": "Successfully logged out"}

@router.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(credentials: str = Depends(security)):
    """Get current user information"""
    from ...core.middleware import get_current_user_and_tenant
    
    user_info = await get_current_user_and_tenant(credentials)
    
    # Get full user details from database
    db = await get_database()
    users_collection = db.get_default_database().users
    user = await users_collection.find_one({
        "_id": user_info["user_id"],
        "tenant_id": user_info["tenant_id"]
    })
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        id=user["_id"],
        username=user["username"],
        email=user["email"],
        full_name=user["full_name"],
        role=user["role"],
        status=user["status"],
        job_title=user.get("job_title"),
        department=user.get("department"),
        phone=user.get("phone"),
        avatar_url=user.get("avatar_url"),
        last_login=user.get("last_login"),
        created_at=user["created_at"],
        updated_at=user["updated_at"]
    )
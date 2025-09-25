from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from .common import BaseDocument
import uuid

class UserRole(str, Enum):
    ADMIN = "admin"                    # Platform administration
    PMO_ADMIN = "pmo_admin"           # PMO-level administration
    PORTFOLIO_MANAGER = "portfolio_manager"  # Portfolio oversight
    PROJECT_MANAGER = "project_manager"      # Project execution
    RESOURCE = "resource"             # Task execution and time tracking
    FINANCE = "finance"               # Budget oversight
    VIEWER = "viewer"                 # Read-only access

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"

class User(BaseDocument):
    """User model"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str
    hashed_password: str
    role: UserRole
    status: UserStatus = UserStatus.PENDING_VERIFICATION
    
    # Profile information
    job_title: Optional[str] = None
    department: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    
    # Permissions and access
    permissions: List[str] = Field(default_factory=list)
    portfolio_access: List[str] = Field(default_factory=list)  # Portfolio IDs user can access
    project_access: List[str] = Field(default_factory=list)    # Project IDs user can access
    
    # Authentication
    last_login: Optional[datetime] = None
    failed_login_attempts: int = 0
    locked_until: Optional[datetime] = None
    password_reset_token: Optional[str] = None
    password_reset_expires: Optional[datetime] = None
    email_verification_token: Optional[str] = None
    
    # Preferences
    preferences: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}

class UserCreate(BaseModel):
    """Schema for creating a new user"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str
    password: str = Field(..., min_length=8)
    role: UserRole
    job_title: Optional[str] = None
    department: Optional[str] = None
    phone: Optional[str] = None

class UserUpdate(BaseModel):
    """Schema for updating user"""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None
    job_title: Optional[str] = None
    department: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    portfolio_access: Optional[List[str]] = None
    project_access: Optional[List[str]] = None

class UserLogin(BaseModel):
    """Schema for user login"""
    username: str
    password: str
    tenant_code: str

class UserResponse(BaseModel):
    """User response model"""
    id: str
    username: str
    email: str
    full_name: str
    role: UserRole
    status: UserStatus
    job_title: Optional[str]
    department: Optional[str]
    phone: Optional[str]
    avatar_url: Optional[str]
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime

class TokenResponse(BaseModel):
    """Token response model"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse

class PasswordReset(BaseModel):
    """Password reset request"""
    email: EmailStr
    tenant_code: str

class PasswordResetConfirm(BaseModel):
    """Password reset confirmation"""
    token: str
    new_password: str = Field(..., min_length=8)
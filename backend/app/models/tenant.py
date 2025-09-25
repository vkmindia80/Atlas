from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

class TenantStatus(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    TRIAL = "trial"
    CANCELLED = "cancelled"

class TenantPlan(str, Enum):
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"

class TenantSettings(BaseModel):
    """Tenant-specific settings"""
    date_format: str = "MM/DD/YYYY"
    time_zone: str = "UTC"
    currency: str = "USD"
    language: str = "en"
    allow_user_registration: bool = False
    require_email_verification: bool = True
    session_timeout_minutes: int = 480  # 8 hours
    password_policy: Dict[str, Any] = Field(default_factory=lambda: {
        "min_length": 8,
        "require_uppercase": True,
        "require_lowercase": True,
        "require_numbers": True,
        "require_special_chars": True
    })

class Tenant(BaseModel):
    """Tenant model for multi-tenancy"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    name: str = Field(..., description="Organization name")
    code: str = Field(..., description="Unique tenant code")
    domain: str = Field(..., description="Organization domain")
    status: TenantStatus = TenantStatus.TRIAL
    plan: TenantPlan = TenantPlan.STARTER
    
    # Contact information
    admin_email: EmailStr
    admin_name: str
    phone: Optional[str] = None
    address: Optional[Dict[str, str]] = None
    
    # Subscription details
    subscription_start: Optional[datetime] = None
    subscription_end: Optional[datetime] = None
    max_users: int = 10
    max_projects: int = 50
    
    # Settings
    settings: TenantSettings = Field(default_factory=TenantSettings)
    
    # SSO Configuration
    sso_enabled: bool = False
    sso_config: Optional[Dict[str, Any]] = None
    
    # Audit fields
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}

class TenantCreate(BaseModel):
    """Schema for creating a new tenant"""
    name: str
    code: str
    domain: str
    admin_email: EmailStr
    admin_name: str
    phone: Optional[str] = None
    plan: TenantPlan = TenantPlan.STARTER

class TenantUpdate(BaseModel):
    """Schema for updating tenant"""
    name: Optional[str] = None
    domain: Optional[str] = None
    admin_email: Optional[EmailStr] = None
    admin_name: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[TenantStatus] = None
    plan: Optional[TenantPlan] = None
    max_users: Optional[int] = None
    max_projects: Optional[int] = None
    settings: Optional[TenantSettings] = None

class TenantResponse(BaseModel):
    """Tenant response model"""
    id: str
    name: str
    code: str
    domain: str
    status: TenantStatus
    plan: TenantPlan
    admin_email: str
    admin_name: str
    max_users: int
    max_projects: int
    created_at: datetime
    updated_at: datetime
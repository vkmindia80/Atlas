from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal
from .common import BaseDocument, Priority, Status, HealthStatus
from enum import Enum

class PortfolioType(str, Enum):
    STRATEGIC = "strategic"
    OPERATIONAL = "operational"
    INNOVATION = "innovation"
    MAINTENANCE = "maintenance"

class StrategicAlignment(BaseModel):
    """Strategic alignment model"""
    objective_id: str
    objective_name: str
    alignment_score: float = Field(..., ge=0, le=1)  # 0-1 score
    contribution_percentage: float = Field(..., ge=0, le=100)

class FinancialMetrics(BaseModel):
    """Portfolio financial metrics"""
    total_budget: Decimal = Field(default=Decimal('0'))
    allocated_budget: Decimal = Field(default=Decimal('0'))
    spent_amount: Decimal = Field(default=Decimal('0'))
    committed_amount: Decimal = Field(default=Decimal('0'))
    forecasted_cost: Decimal = Field(default=Decimal('0'))
    npv: Optional[Decimal] = None
    irr: Optional[float] = None
    roi_percentage: Optional[float] = None
    payback_period_months: Optional[int] = None

class RiskMetrics(BaseModel):
    """Portfolio risk metrics"""
    risk_score: float = Field(default=0.0, ge=0, le=1)  # 0-1 composite score
    high_risks_count: int = Field(default=0)
    medium_risks_count: int = Field(default=0)
    low_risks_count: int = Field(default=0)
    overdue_risks_count: int = Field(default=0)

class Portfolio(BaseDocument):
    """Portfolio model"""
    name: str = Field(..., max_length=200)
    code: str = Field(..., max_length=50)  # Unique within tenant
    description: Optional[str] = None
    
    # Classification
    portfolio_type: PortfolioType
    status: Status = Status.DRAFT
    health_status: HealthStatus = HealthStatus.GREEN
    priority: Priority = Priority.MEDIUM
    
    # Ownership and governance
    portfolio_manager_id: str
    sponsors: List[str] = Field(default_factory=list)  # User IDs
    stakeholders: List[str] = Field(default_factory=list)  # User IDs
    
    # Strategic alignment
    strategic_objectives: List[StrategicAlignment] = Field(default_factory=list)
    business_case_url: Optional[str] = None
    
    # Timeline
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    
    # Financial information
    financial_metrics: FinancialMetrics = Field(default_factory=FinancialMetrics)
    
    # Risk information
    risk_metrics: RiskMetrics = Field(default_factory=RiskMetrics)
    
    # Project references
    project_ids: List[str] = Field(default_factory=list)
    
    # Configuration
    settings: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }

class PortfolioCreate(BaseModel):
    """Schema for creating a new portfolio"""
    name: str = Field(..., max_length=200)
    code: str = Field(..., max_length=50)
    description: Optional[str] = None
    portfolio_type: PortfolioType
    priority: Priority = Priority.MEDIUM
    portfolio_manager_id: str
    sponsors: List[str] = Field(default_factory=list)
    stakeholders: List[str] = Field(default_factory=list)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    business_case_url: Optional[str] = None

class PortfolioUpdate(BaseModel):
    """Schema for updating portfolio"""
    name: Optional[str] = None
    description: Optional[str] = None
    portfolio_type: Optional[PortfolioType] = None
    status: Optional[Status] = None
    health_status: Optional[HealthStatus] = None
    priority: Optional[Priority] = None
    portfolio_manager_id: Optional[str] = None
    sponsors: Optional[List[str]] = None
    stakeholders: Optional[List[str]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    business_case_url: Optional[str] = None
    strategic_objectives: Optional[List[StrategicAlignment]] = None

class PortfolioResponse(BaseModel):
    """Portfolio response model"""
    id: str
    name: str
    code: str
    description: Optional[str]
    portfolio_type: PortfolioType
    status: Status
    health_status: HealthStatus
    priority: Priority
    portfolio_manager_id: str
    sponsors: List[str]
    stakeholders: List[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    financial_metrics: FinancialMetrics
    risk_metrics: RiskMetrics
    project_count: int = 0
    created_at: datetime
    updated_at: datetime

class PortfolioDashboard(BaseModel):
    """Portfolio dashboard data"""
    portfolio: PortfolioResponse
    project_summary: Dict[str, int]  # Status counts
    budget_utilization: Dict[str, float]
    timeline_progress: float
    top_risks: List[Dict[str, Any]]
    recent_activities: List[Dict[str, Any]]
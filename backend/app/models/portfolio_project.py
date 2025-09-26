from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from decimal import Decimal
from .common import BaseDocument, Priority, Status
from enum import Enum

class PortfolioProjectRelationshipType(str, Enum):
    PRIMARY = "primary"          # Project directly belongs to portfolio
    SECONDARY = "secondary"      # Project has secondary relationship
    DEPENDENCY = "dependency"    # Project is a dependency
    SHARED = "shared"           # Project shared across portfolios

class PortfolioProjectStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PROPOSED = "proposed"
    APPROVED = "approved"
    REJECTED = "rejected"

class ResourceAllocationRule(BaseModel):
    """Rules for resource allocation from portfolio to project"""
    max_budget_percentage: Optional[float] = None  # Max % of portfolio budget
    max_team_size: Optional[int] = None
    priority_multiplier: float = 1.0  # Affects resource priority
    
class PortfolioProject(BaseDocument):
    """Portfolio-Project relationship with enhanced management"""
    # Core relationship
    portfolio_id: str
    project_id: str
    
    # Relationship details
    relationship_type: PortfolioProjectRelationshipType = PortfolioProjectRelationshipType.PRIMARY
    status: PortfolioProjectStatus = PortfolioProjectStatus.ACTIVE
    
    # Financial allocation
    allocated_budget: Decimal = Field(default=Decimal('0'))
    budget_percentage: Optional[float] = None  # Percentage of portfolio budget
    
    # Strategic alignment
    strategic_objective_ids: List[str] = Field(default_factory=list)
    alignment_score: float = Field(default=0.0, ge=0, le=1)  # 0-1 strategic alignment
    contribution_weight: float = Field(default=1.0, ge=0)  # Project's weight in portfolio
    
    # Timeline alignment
    portfolio_phase: Optional[str] = None
    expected_value_delivery_date: Optional[date] = None
    
    # Resource allocation rules
    resource_rules: ResourceAllocationRule = Field(default_factory=ResourceAllocationRule)
    
    # Governance
    review_frequency_days: int = 30  # How often to review this relationship
    last_review_date: Optional[datetime] = None
    next_review_date: Optional[datetime] = None
    
    # Performance tracking
    value_delivered: Decimal = Field(default=Decimal('0'))
    roi_calculation: Optional[float] = None
    risk_adjusted_value: Optional[Decimal] = None
    
    # Dependencies within portfolio
    dependent_project_ids: List[str] = Field(default_factory=list)
    dependency_project_ids: List[str] = Field(default_factory=list)
    
    # Notes and comments
    relationship_notes: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }

class PortfolioProjectCreate(BaseModel):
    """Schema for creating portfolio-project relationship"""
    portfolio_id: str
    project_id: str
    relationship_type: PortfolioProjectRelationshipType = PortfolioProjectRelationshipType.PRIMARY
    allocated_budget: Optional[Decimal] = None
    budget_percentage: Optional[float] = None
    strategic_objective_ids: List[str] = Field(default_factory=list)
    alignment_score: Optional[float] = None
    contribution_weight: Optional[float] = None
    portfolio_phase: Optional[str] = None
    expected_value_delivery_date: Optional[date] = None
    relationship_notes: Optional[str] = None

class PortfolioProjectUpdate(BaseModel):
    """Schema for updating portfolio-project relationship"""
    relationship_type: Optional[PortfolioProjectRelationshipType] = None
    status: Optional[PortfolioProjectStatus] = None
    allocated_budget: Optional[Decimal] = None
    budget_percentage: Optional[float] = None
    strategic_objective_ids: Optional[List[str]] = None
    alignment_score: Optional[float] = None
    contribution_weight: Optional[float] = None
    portfolio_phase: Optional[str] = None
    expected_value_delivery_date: Optional[date] = None
    value_delivered: Optional[Decimal] = None
    roi_calculation: Optional[float] = None
    dependent_project_ids: Optional[List[str]] = None
    dependency_project_ids: Optional[List[str]] = None
    relationship_notes: Optional[str] = None

class PortfolioProjectResponse(BaseModel):
    """Portfolio-project relationship response"""
    id: str
    portfolio_id: str
    project_id: str
    relationship_type: PortfolioProjectRelationshipType
    status: PortfolioProjectStatus
    allocated_budget: Decimal
    budget_percentage: Optional[float]
    strategic_objective_ids: List[str]
    alignment_score: float
    contribution_weight: float
    portfolio_phase: Optional[str]
    expected_value_delivery_date: Optional[date]
    value_delivered: Decimal
    roi_calculation: Optional[float]
    dependent_project_ids: List[str]
    dependency_project_ids: List[str]
    last_review_date: Optional[datetime]
    next_review_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

class PortfolioAnalytics(BaseModel):
    """Portfolio analytics and KPIs"""
    portfolio_id: str
    
    # Project metrics
    total_projects: int
    active_projects: int
    completed_projects: int
    on_hold_projects: int
    cancelled_projects: int
    
    # Financial metrics
    total_budget: Decimal
    total_allocated: Decimal
    total_spent: Decimal
    budget_utilization: float
    average_project_budget: Decimal
    
    # Timeline metrics
    projects_on_schedule: int
    projects_delayed: int
    average_project_duration: float
    
    # Value metrics
    total_value_delivered: Decimal
    average_roi: float
    strategic_alignment_avg: float
    
    # Risk metrics
    high_risk_projects: int
    medium_risk_projects: int
    low_risk_projects: int
    overall_portfolio_risk: float
    
    # Resource metrics
    total_team_members: int
    average_team_utilization: float
    
    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }

class PortfolioDependencyMap(BaseModel):
    """Portfolio dependency mapping"""
    portfolio_id: str
    project_dependencies: List[Dict[str, Any]]  # Graph structure
    critical_path_projects: List[str]
    dependency_risks: List[Dict[str, Any]]
    
class BulkPortfolioProjectOperation(BaseModel):
    """Bulk operations for portfolio-project relationships"""
    operation: str  # "add", "remove", "update_budget", "update_alignment"
    portfolio_id: str
    project_ids: List[str]
    operation_data: Dict[str, Any]  # Operation-specific data
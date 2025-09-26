from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from decimal import Decimal
from .common import BaseDocument, Priority, Status, HealthStatus
from .portfolio import PortfolioType, FinancialMetrics, RiskMetrics, StrategicAlignment
from enum import Enum

class PortfolioProject(BaseDocument):
    """Association model for portfolio-project relationships"""
    portfolio_id: str
    project_id: str
    
    # Relationship metadata
    added_date: date = Field(default_factory=lambda: datetime.now().date())
    strategic_weight: float = Field(default=1.0, ge=0, le=1)  # Strategic importance weight
    budget_allocation: Optional[Decimal] = None
    priority_ranking: Optional[int] = None
    
    # Strategic alignment scoring
    alignment_scores: Dict[str, float] = Field(default_factory=dict)  # objective_id -> score
    
    # Status tracking
    is_active: bool = True
    removed_date: Optional[date] = None
    removal_reason: Optional[str] = None

class PortfolioKPI(BaseModel):
    """Portfolio Key Performance Indicator"""
    id: str = Field(default_factory=lambda: str(__import__('uuid').uuid4()))
    name: str
    description: Optional[str] = None
    kpi_type: str  # "financial", "schedule", "scope", "quality", "risk"
    
    # Measurement
    unit: str  # "percentage", "currency", "count", "days"
    target_value: float
    current_value: float = 0.0
    baseline_value: Optional[float] = None
    
    # Thresholds
    red_threshold: Optional[float] = None
    yellow_threshold: Optional[float] = None
    green_threshold: Optional[float] = None
    
    # Tracking
    calculation_method: Optional[str] = None
    update_frequency: str = "monthly"  # "daily", "weekly", "monthly", "quarterly"
    last_updated: Optional[datetime] = None

class PortfolioBudgetCategory(BaseModel):
    """Portfolio budget category breakdown"""
    category_name: str
    allocated_amount: Decimal = Field(default=Decimal('0'))
    spent_amount: Decimal = Field(default=Decimal('0'))
    committed_amount: Decimal = Field(default=Decimal('0'))
    forecasted_amount: Decimal = Field(default=Decimal('0'))
    
    # Category metadata
    description: Optional[str] = None
    is_mandatory: bool = False
    approval_required: bool = False

class PortfolioCapacity(BaseModel):
    """Portfolio resource capacity model"""
    id: str = Field(default_factory=lambda: str(__import__('uuid').uuid4()))
    resource_type: str  # "project_manager", "developer", "analyst", etc.
    total_capacity: float  # Total FTE available
    allocated_capacity: float = 0.0  # Currently allocated FTE
    
    # Time period
    period_start: date
    period_end: date
    
    # Utilization metrics
    utilization_percentage: float = 0.0
    overallocation_hours: float = 0.0

class EnhancedPortfolio(BaseDocument):
    """Enhanced portfolio model with advanced features"""
    # Basic information
    name: str = Field(..., max_length=200)
    code: str = Field(..., max_length=50)
    description: Optional[str] = None
    
    # Classification
    portfolio_type: PortfolioType
    status: Status = Status.DRAFT
    health_status: HealthStatus = HealthStatus.GREEN
    priority: Priority = Priority.MEDIUM
    
    # Ownership and governance
    portfolio_manager_id: str
    sponsors: List[str] = Field(default_factory=list)
    stakeholders: List[str] = Field(default_factory=list)
    
    # Strategic alignment
    strategic_objectives: List[StrategicAlignment] = Field(default_factory=list)
    business_case_url: Optional[str] = None
    
    # Timeline
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    
    # Enhanced financial management
    financial_metrics: FinancialMetrics = Field(default_factory=FinancialMetrics)
    budget_categories: List[PortfolioBudgetCategory] = Field(default_factory=list)
    
    # Risk management
    risk_metrics: RiskMetrics = Field(default_factory=RiskMetrics)
    risk_tolerance: str = "medium"  # "low", "medium", "high"
    
    # Performance tracking
    kpis: List[PortfolioKPI] = Field(default_factory=list)
    
    # Resource management
    capacity_planning: List[PortfolioCapacity] = Field(default_factory=list)
    
    # Project portfolio management
    project_selection_criteria: Dict[str, Any] = Field(default_factory=dict)
    max_concurrent_projects: Optional[int] = None
    
    # Reporting and dashboards
    reporting_schedule: str = "monthly"  # "weekly", "monthly", "quarterly"
    dashboard_config: Dict[str, Any] = Field(default_factory=dict)
    
    # Communication
    last_board_meeting: Optional[date] = None
    next_board_meeting: Optional[date] = None
    meeting_frequency: str = "monthly"
    
    # Configuration
    settings: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }

class PortfolioSnapshot(BaseModel):
    """Portfolio performance snapshot for reporting"""
    id: str = Field(default_factory=lambda: str(__import__('uuid').uuid4()))
    portfolio_id: str
    snapshot_date: date = Field(default_factory=lambda: datetime.now().date())
    created_by: str
    
    # Financial snapshot
    financial_snapshot: FinancialMetrics
    budget_utilization: float  # Percentage of budget utilized
    
    # Project metrics
    total_projects: int
    active_projects: int
    completed_projects: int
    on_hold_projects: int
    cancelled_projects: int
    
    # Health metrics
    projects_on_track: int
    projects_at_risk: int
    projects_critical: int
    
    # KPI snapshot
    kpi_values: Dict[str, float] = Field(default_factory=dict)  # kpi_id -> current_value
    
    # Risk snapshot
    risk_snapshot: RiskMetrics
    
    # Variance analysis
    schedule_variance_avg: float = 0.0  # Average schedule variance across projects
    cost_variance_avg: float = 0.0  # Average cost variance across projects
    
    # Comments and notes
    executive_summary: Optional[str] = None
    key_achievements: List[str] = Field(default_factory=list)
    major_issues: List[str] = Field(default_factory=list)
    action_items: List[str] = Field(default_factory=list)

# Response models for enhanced portfolio features
class EnhancedPortfolioResponse(BaseModel):
    """Enhanced portfolio response model"""
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
    start_date: Optional[date]
    end_date: Optional[date]
    financial_metrics: FinancialMetrics
    risk_metrics: RiskMetrics
    kpis: List[PortfolioKPI]
    project_count: int = 0
    active_project_count: int = 0
    budget_utilization_percentage: float = 0.0
    created_at: datetime
    updated_at: datetime

class PortfolioProjectResponse(BaseModel):
    """Portfolio-project relationship response"""
    id: str
    portfolio_id: str
    project_id: str
    project_name: str
    project_status: Status
    strategic_weight: float
    budget_allocation: Optional[Decimal]
    priority_ranking: Optional[int]
    alignment_scores: Dict[str, float]
    added_date: date
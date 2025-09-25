from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from decimal import Decimal
from .common import BaseDocument, Priority, Status, HealthStatus
from enum import Enum

class ProjectType(str, Enum):
    SOFTWARE_DEVELOPMENT = "software_development"
    INFRASTRUCTURE = "infrastructure"
    RESEARCH = "research"
    MARKETING = "marketing"
    PROCESS_IMPROVEMENT = "process_improvement"
    COMPLIANCE = "compliance"
    OTHER = "other"

class ProjectMethodology(str, Enum):
    WATERFALL = "waterfall"
    AGILE = "agile"
    SCRUM = "scrum"
    KANBAN = "kanban"
    HYBRID = "hybrid"
    LEAN = "lean"

class MilestoneStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DELAYED = "delayed"
    CANCELLED = "cancelled"

class Milestone(BaseModel):
    """Project milestone model"""
    id: str = Field(default_factory=lambda: str(__import__('uuid').uuid4()))
    name: str
    description: Optional[str] = None
    planned_date: date
    actual_date: Optional[date] = None
    status: MilestoneStatus = MilestoneStatus.PLANNED
    deliverables: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)  # Other milestone IDs
    
class ProjectFinancials(BaseModel):
    """Project financial information"""
    total_budget: Decimal = Field(default=Decimal('0'))
    allocated_budget: Decimal = Field(default=Decimal('0'))
    spent_amount: Decimal = Field(default=Decimal('0'))
    committed_amount: Decimal = Field(default=Decimal('0'))
    forecasted_cost: Decimal = Field(default=Decimal('0'))
    budget_variance: Decimal = Field(default=Decimal('0'))
    cost_to_complete: Decimal = Field(default=Decimal('0'))
    
    # Cost categories
    labor_cost: Decimal = Field(default=Decimal('0'))
    material_cost: Decimal = Field(default=Decimal('0'))
    vendor_cost: Decimal = Field(default=Decimal('0'))
    overhead_cost: Decimal = Field(default=Decimal('0'))
    
class ResourceAllocation(BaseModel):
    """Resource allocation model"""
    user_id: str
    role: str
    allocation_percentage: float = Field(..., ge=0, le=100)
    hourly_rate: Optional[Decimal] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    skills_required: List[str] = Field(default_factory=list)

class Project(BaseDocument):
    """Project model"""
    name: str = Field(..., max_length=200)
    code: str = Field(..., max_length=50)  # Unique within tenant
    description: Optional[str] = None
    
    # Classification
    project_type: ProjectType
    methodology: ProjectMethodology = ProjectMethodology.AGILE
    status: Status = Status.DRAFT
    health_status: HealthStatus = HealthStatus.GREEN
    priority: Priority = Priority.MEDIUM
    
    # Hierarchy
    portfolio_id: Optional[str] = None
    parent_project_id: Optional[str] = None
    
    # Ownership
    project_manager_id: str
    sponsor_id: Optional[str] = None
    team_members: List[str] = Field(default_factory=list)  # User IDs
    
    # Timeline
    planned_start_date: Optional[date] = None
    planned_end_date: Optional[date] = None
    actual_start_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    
    # Progress tracking
    percent_complete: float = Field(default=0.0, ge=0, le=100)
    milestones: List[Milestone] = Field(default_factory=list)
    
    # Financial information
    financials: ProjectFinancials = Field(default_factory=ProjectFinancials)
    
    # Resource management
    resource_allocations: List[ResourceAllocation] = Field(default_factory=list)
    
    # Risk and issues
    risk_score: float = Field(default=0.0, ge=0, le=1)
    open_issues_count: int = Field(default=0)
    open_risks_count: int = Field(default=0)
    
    # Documents and attachments
    document_urls: List[str] = Field(default_factory=list)
    
    # Custom fields for extensibility
    custom_fields: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }

class ProjectCreate(BaseModel):
    """Schema for creating a new project"""
    name: str = Field(..., max_length=200)
    code: str = Field(..., max_length=50)
    description: Optional[str] = None
    project_type: ProjectType
    methodology: ProjectMethodology = ProjectMethodology.AGILE
    priority: Priority = Priority.MEDIUM
    portfolio_id: Optional[str] = None
    parent_project_id: Optional[str] = None
    project_manager_id: str
    sponsor_id: Optional[str] = None
    planned_start_date: Optional[date] = None
    planned_end_date: Optional[date] = None

class ProjectUpdate(BaseModel):
    """Schema for updating project"""
    name: Optional[str] = None
    description: Optional[str] = None
    project_type: Optional[ProjectType] = None
    methodology: Optional[ProjectMethodology] = None
    status: Optional[Status] = None
    health_status: Optional[HealthStatus] = None
    priority: Optional[Priority] = None
    portfolio_id: Optional[str] = None
    project_manager_id: Optional[str] = None
    sponsor_id: Optional[str] = None
    planned_start_date: Optional[date] = None
    planned_end_date: Optional[date] = None
    actual_start_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    percent_complete: Optional[float] = None
    team_members: Optional[List[str]] = None

class ProjectResponse(BaseModel):
    """Project response model"""
    id: str
    name: str
    code: str
    description: Optional[str]
    project_type: ProjectType
    methodology: ProjectMethodology
    status: Status
    health_status: HealthStatus
    priority: Priority
    portfolio_id: Optional[str]
    project_manager_id: str
    sponsor_id: Optional[str]
    planned_start_date: Optional[date]
    planned_end_date: Optional[date]
    actual_start_date: Optional[date]
    actual_end_date: Optional[date]
    percent_complete: float
    financials: ProjectFinancials
    risk_score: float
    open_issues_count: int
    open_risks_count: int
    team_size: int = 0
    created_at: datetime
    updated_at: datetime

class ProjectDashboard(BaseModel):
    """Project dashboard data"""
    project: ProjectResponse
    milestone_progress: Dict[str, int]
    budget_status: Dict[str, float]
    team_utilization: Dict[str, float]
    recent_activities: List[Dict[str, Any]]
    upcoming_milestones: List[Milestone]
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime, date
from decimal import Decimal
from .common import BaseDocument, Priority, Status, HealthStatus
from .project import ProjectType, ProjectMethodology, MilestoneStatus, Milestone, ProjectFinancials, ResourceAllocation
from enum import Enum

class ProjectPhase(str, Enum):
    INITIATION = "initiation"
    PLANNING = "planning"
    EXECUTION = "execution"
    MONITORING = "monitoring"
    CLOSURE = "closure"

class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

class DependencyType(str, Enum):
    FINISH_TO_START = "finish_to_start"
    START_TO_START = "start_to_start"
    FINISH_TO_FINISH = "finish_to_finish"
    START_TO_FINISH = "start_to_finish"

class TaskStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class IssueType(str, Enum):
    BUG = "bug"
    TASK = "task"
    STORY = "story"
    EPIC = "epic"
    IMPROVEMENT = "improvement"
    BLOCKER = "blocker"

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ProjectDependency(BaseModel):
    """Project dependency model"""
    id: str = Field(default_factory=lambda: str(__import__('uuid').uuid4()))
    predecessor_project_id: Optional[str] = None
    predecessor_task_id: Optional[str] = None
    successor_project_id: Optional[str] = None
    successor_task_id: Optional[str] = None
    dependency_type: DependencyType = DependencyType.FINISH_TO_START
    lag_days: int = 0  # Lag time in days
    description: Optional[str] = None
    is_critical_path: bool = False

class ProjectTask(BaseModel):
    """Enhanced task model with dependencies"""
    id: str = Field(default_factory=lambda: str(__import__('uuid').uuid4()))
    name: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.NOT_STARTED
    priority: Priority = Priority.MEDIUM
    
    # Assignment
    assignee_id: Optional[str] = None
    reviewer_id: Optional[str] = None
    
    # Timeline
    planned_start_date: Optional[date] = None
    planned_end_date: Optional[date] = None
    actual_start_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    
    # Effort estimation
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    percent_complete: float = Field(default=0.0, ge=0, le=100)
    
    # Hierarchy
    parent_task_id: Optional[str] = None
    subtasks: List[str] = Field(default_factory=list)  # Task IDs
    
    # Dependencies
    dependencies: List[ProjectDependency] = Field(default_factory=list)
    
    # Tags and labels
    labels: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    
    # Story points for agile projects
    story_points: Optional[int] = None
    
    class Config:
        json_encoders = {
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat()
        }

class ProjectIssue(BaseModel):
    """Project issue/bug tracking"""
    id: str = Field(default_factory=lambda: str(__import__('uuid').uuid4()))
    title: str
    description: Optional[str] = None
    issue_type: IssueType
    status: Status = Status.ACTIVE
    priority: Priority = Priority.MEDIUM
    
    # Assignment
    reporter_id: str
    assignee_id: Optional[str] = None
    
    # Timeline
    created_date: date = Field(default_factory=lambda: datetime.now().date())
    due_date: Optional[date] = None
    resolved_date: Optional[date] = None
    
    # Relationships
    related_task_id: Optional[str] = None
    blocked_tasks: List[str] = Field(default_factory=list)
    
    # Resolution
    resolution: Optional[str] = None
    resolution_notes: Optional[str] = None
    
    # Metadata
    labels: List[str] = Field(default_factory=list)
    estimated_hours: Optional[float] = None

class ProjectRisk(BaseModel):
    """Project risk management"""
    id: str = Field(default_factory=lambda: str(__import__('uuid').uuid4()))
    title: str
    description: str
    risk_level: RiskLevel
    probability: float = Field(..., ge=0, le=1)  # 0-1 probability
    impact: float = Field(..., ge=0, le=1)  # 0-1 impact score
    
    # Ownership
    owner_id: str
    identified_by: str
    identified_date: date = Field(default_factory=lambda: datetime.now().date())
    
    # Status tracking
    status: Status = Status.ACTIVE
    
    # Mitigation
    mitigation_plan: Optional[str] = None
    contingency_plan: Optional[str] = None
    mitigation_cost: Optional[Decimal] = None
    
    # Timeline
    target_resolution_date: Optional[date] = None
    actual_resolution_date: Optional[date] = None
    
    # Impact areas
    affected_tasks: List[str] = Field(default_factory=list)
    affected_milestones: List[str] = Field(default_factory=list)

class ProjectApproval(BaseModel):
    """Project approval workflow"""
    id: str = Field(default_factory=lambda: str(__import__('uuid').uuid4()))
    approval_type: str  # "initiation", "baseline", "change_request", "closure"
    status: ApprovalStatus = ApprovalStatus.PENDING
    
    # Request details
    requested_by: str
    request_date: datetime = Field(default_factory=datetime.utcnow)
    description: str
    justification: Optional[str] = None
    
    # Approval workflow
    approver_id: str
    approval_date: Optional[datetime] = None
    approval_comments: Optional[str] = None
    
    # Attached documents
    document_urls: List[str] = Field(default_factory=list)

class ProjectBaseline(BaseModel):
    """Project baseline snapshot"""
    id: str = Field(default_factory=lambda: str(__import__('uuid').uuid4()))
    name: str
    description: Optional[str] = None
    baseline_date: date = Field(default_factory=lambda: datetime.now().date())
    created_by: str
    
    # Baseline data snapshot
    planned_start_date: Optional[date] = None
    planned_end_date: Optional[date] = None
    total_budget: Decimal = Field(default=Decimal('0'))
    milestones_snapshot: List[Milestone] = Field(default_factory=list)
    tasks_snapshot: List[ProjectTask] = Field(default_factory=list)
    resource_snapshot: List[ResourceAllocation] = Field(default_factory=list)
    
    # Comparison metrics (calculated fields)
    schedule_variance_days: Optional[int] = None
    cost_variance: Optional[Decimal] = None
    scope_change_count: int = 0

class ProjectTemplate(BaseModel):
    """Project template for standardized project creation"""
    id: str = Field(default_factory=lambda: str(__import__('uuid').uuid4()))
    name: str
    description: Optional[str] = None
    project_type: ProjectType
    methodology: ProjectMethodology
    
    # Template data
    template_tasks: List[ProjectTask] = Field(default_factory=list)
    template_milestones: List[Milestone] = Field(default_factory=list)
    template_phases: List[str] = Field(default_factory=list)
    
    # Default settings
    default_duration_days: Optional[int] = None
    default_budget: Optional[Decimal] = None
    required_roles: List[str] = Field(default_factory=list)
    
    # Usage tracking
    usage_count: int = 0
    is_active: bool = True
    created_by: str

class EnhancedProject(BaseDocument):
    """Enhanced project model with lifecycle management"""
    # Basic information (inherited from original Project)
    name: str = Field(..., max_length=200)
    code: str = Field(..., max_length=50)
    description: Optional[str] = None
    
    # Classification
    project_type: ProjectType
    methodology: ProjectMethodology = ProjectMethodology.AGILE
    status: Status = Status.DRAFT
    health_status: HealthStatus = HealthStatus.GREEN
    priority: Priority = Priority.MEDIUM
    
    # Lifecycle phase
    current_phase: ProjectPhase = ProjectPhase.INITIATION
    
    # Hierarchy
    portfolio_id: Optional[str] = None
    parent_project_id: Optional[str] = None
    template_id: Optional[str] = None  # Reference to template used
    
    # Ownership
    project_manager_id: str
    sponsor_id: Optional[str] = None
    team_members: List[str] = Field(default_factory=list)
    
    # Timeline
    planned_start_date: Optional[date] = None
    planned_end_date: Optional[date] = None
    actual_start_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    
    # Progress tracking
    percent_complete: float = Field(default=0.0, ge=0, le=100)
    milestones: List[Milestone] = Field(default_factory=list)
    tasks: List[ProjectTask] = Field(default_factory=list)
    
    # Financial information
    financials: ProjectFinancials = Field(default_factory=ProjectFinancials)
    
    # Resource management
    resource_allocations: List[ResourceAllocation] = Field(default_factory=list)
    
    # Risk and issue management
    risks: List[ProjectRisk] = Field(default_factory=list)
    issues: List[ProjectIssue] = Field(default_factory=list)
    risk_score: float = Field(default=0.0, ge=0, le=1)
    
    # Dependencies
    dependencies: List[ProjectDependency] = Field(default_factory=list)
    
    # Approval workflow
    approvals: List[ProjectApproval] = Field(default_factory=list)
    requires_approval: bool = True
    
    # Baseline management
    baselines: List[ProjectBaseline] = Field(default_factory=list)
    current_baseline_id: Optional[str] = None
    
    # Documents and attachments
    document_urls: List[str] = Field(default_factory=list)
    
    # Communication
    last_status_update: Optional[str] = None
    last_status_date: Optional[date] = None
    
    # Custom fields for extensibility
    custom_fields: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }

class ProjectIntakeForm(BaseModel):
    """Project intake/request form"""
    # Basic project information
    project_name: str = Field(..., max_length=200)
    business_justification: str
    project_type: ProjectType
    methodology: ProjectMethodology = ProjectMethodology.AGILE
    priority: Priority = Priority.MEDIUM
    
    # Timeline
    requested_start_date: Optional[date] = None
    target_end_date: Optional[date] = None
    
    # Financial
    estimated_budget: Optional[Decimal] = None
    budget_source: Optional[str] = None
    
    # Stakeholders
    project_sponsor: str
    business_owner: str
    preferred_project_manager: Optional[str] = None
    
    # Strategic alignment
    portfolio_id: Optional[str] = None
    strategic_objectives: List[str] = Field(default_factory=list)  # Objective IDs
    
    # Scope and requirements
    project_scope: str
    key_requirements: List[str] = Field(default_factory=list)
    success_criteria: List[str] = Field(default_factory=list)
    
    # Resources
    estimated_team_size: Optional[int] = None
    required_skills: List[str] = Field(default_factory=list)
    
    # Risk assessment
    identified_risks: List[str] = Field(default_factory=list)
    risk_mitigation_notes: Optional[str] = None
    
    # Additional information
    business_case_url: Optional[str] = None
    supporting_documents: List[str] = Field(default_factory=list)
    
class ProjectCreateFromIntake(BaseModel):
    """Schema for creating project from intake form"""
    intake_data: ProjectIntakeForm
    template_id: Optional[str] = None
    auto_approve: bool = False
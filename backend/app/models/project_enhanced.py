from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from decimal import Decimal
from .common import BaseDocument, Priority, Status, HealthStatus
from .project import ProjectType, ProjectMethodology
from enum import Enum

class ProjectPhaseStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"

class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_REVISION = "needs_revision"

class ProjectPhase(BaseModel):
    """Project phase model"""
    id: str = Field(default_factory=lambda: str(__import__('uuid').uuid4()))
    name: str
    description: Optional[str] = None
    phase_order: int
    status: ProjectPhaseStatus = ProjectPhaseStatus.NOT_STARTED
    planned_start_date: Optional[date] = None
    planned_end_date: Optional[date] = None
    actual_start_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    budget_allocated: Decimal = Field(default=Decimal('0'))
    deliverables: List[str] = Field(default_factory=list)
    success_criteria: List[str] = Field(default_factory=list)
    
class ProjectBaseline(BaseModel):
    """Project baseline snapshot"""
    id: str = Field(default_factory=lambda: str(__import__('uuid').uuid4()))
    name: str
    description: Optional[str] = None
    baseline_date: datetime = Field(default_factory=datetime.utcnow)
    created_by: str
    
    # Baseline data
    planned_start_date: Optional[date] = None
    planned_end_date: Optional[date] = None
    total_budget: Decimal = Field(default=Decimal('0'))
    scope_description: Optional[str] = None
    key_milestones: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Snapshot metadata
    is_current_baseline: bool = False
    
class ProjectApproval(BaseModel):
    """Project approval workflow"""
    id: str = Field(default_factory=lambda: str(__import__('uuid').uuid4()))
    approval_type: str  # "initiation", "phase_gate", "scope_change", "budget_change"
    status: ApprovalStatus = ApprovalStatus.PENDING
    requested_by: str
    requested_date: datetime = Field(default_factory=datetime.utcnow)
    
    # Approval details
    title: str
    description: Optional[str] = None
    justification: Optional[str] = None
    impact_analysis: Optional[str] = None
    
    # Approvers
    required_approvers: List[str] = Field(default_factory=list)  # User IDs
    approvals_received: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Timeline
    due_date: Optional[datetime] = None
    approved_date: Optional[datetime] = None
    rejected_date: Optional[datetime] = None

class ProjectTemplate(BaseDocument):
    """Project template for standardization"""
    name: str = Field(..., max_length=200)
    description: Optional[str] = None
    project_type: ProjectType
    methodology: ProjectMethodology
    
    # Template structure
    phases: List[ProjectPhase] = Field(default_factory=list)
    default_milestones: List[Dict[str, Any]] = Field(default_factory=list)
    task_templates: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Configuration
    estimated_duration_days: Optional[int] = None
    estimated_budget: Optional[Decimal] = None
    required_skills: List[str] = Field(default_factory=list)
    
    # Usage tracking
    usage_count: int = 0
    is_active: bool = True

class ProjectIntakeForm(BaseDocument):
    """Project intake form for project requests"""
    # Request details
    project_title: str
    business_justification: str
    project_description: str
    expected_benefits: str
    
    # Requestor information
    requestor_id: str
    requestor_department: str
    sponsor_id: Optional[str] = None
    
    # Project details
    project_type: ProjectType
    priority: Priority
    requested_start_date: Optional[date] = None
    requested_end_date: Optional[date] = None
    estimated_budget: Optional[Decimal] = None
    
    # Requirements
    functional_requirements: List[str] = Field(default_factory=list)
    non_functional_requirements: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    
    # Resources
    required_skills: List[str] = Field(default_factory=list)
    estimated_team_size: Optional[int] = None
    
    # Risk assessment
    identified_risks: List[str] = Field(default_factory=list)
    risk_level: str = "medium"  # low, medium, high, critical
    
    # Approval workflow
    status: ApprovalStatus = ApprovalStatus.PENDING
    approvals: List[ProjectApproval] = Field(default_factory=list)
    
    # Decision
    decision_date: Optional[datetime] = None
    decision_notes: Optional[str] = None
    approved_budget: Optional[Decimal] = None
    assigned_pm: Optional[str] = None

class ProjectSnapshot(BaseDocument):
    """Project snapshot for point-in-time reporting"""
    project_id: str
    snapshot_date: datetime = Field(default_factory=datetime.utcnow)
    snapshot_type: str  # "weekly", "monthly", "milestone", "ad_hoc"
    
    # Status at snapshot time
    status: Status
    health_status: HealthStatus
    percent_complete: float
    
    # Financial snapshot
    budget_spent: Decimal = Field(default=Decimal('0'))
    budget_committed: Decimal = Field(default=Decimal('0'))
    budget_variance: Decimal = Field(default=Decimal('0'))
    
    # Timeline snapshot
    schedule_variance_days: int = 0
    critical_path_delay: int = 0
    
    # Team snapshot
    team_size: int = 0
    team_utilization: float = 0.0
    
    # Progress metrics
    tasks_completed: int = 0
    tasks_remaining: int = 0
    milestones_completed: int = 0
    milestones_remaining: int = 0
    
    # Issues and risks
    open_issues: int = 0
    open_risks: int = 0
    risk_score: float = 0.0
    
    # Comments and notes
    status_notes: Optional[str] = None
    achievements: List[str] = Field(default_factory=list)
    challenges: List[str] = Field(default_factory=list)
    next_period_plans: List[str] = Field(default_factory=list)

# Enhanced project model with lifecycle management
class ProjectEnhanced(BaseDocument):
    """Enhanced project model with full lifecycle support"""
    # Basic project information (inherited from base project model)
    name: str = Field(..., max_length=200)
    code: str = Field(..., max_length=50)
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
    program_id: Optional[str] = None
    
    # Ownership
    project_manager_id: str
    sponsor_id: Optional[str] = None
    team_members: List[str] = Field(default_factory=list)
    
    # Lifecycle management
    phases: List[ProjectPhase] = Field(default_factory=list)
    current_phase_id: Optional[str] = None
    
    # Baseline management
    baselines: List[ProjectBaseline] = Field(default_factory=list)
    current_baseline_id: Optional[str] = None
    
    # Approval workflow
    approvals: List[ProjectApproval] = Field(default_factory=list)
    
    # Template reference
    template_id: Optional[str] = None
    
    # Financial tracking (enhanced)
    financial_metrics: Dict[str, Any] = Field(default_factory=dict)
    
    # Timeline (enhanced)
    planned_start_date: Optional[date] = None
    planned_end_date: Optional[date] = None
    actual_start_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    
    # Progress tracking
    percent_complete: float = Field(default=0.0, ge=0, le=100)
    
    # Custom fields for flexibility
    custom_fields: Dict[str, Any] = Field(default_factory=dict)

# Response models
class ProjectTemplateResponse(BaseModel):
    """Project template response"""
    id: str
    name: str
    description: Optional[str]
    project_type: ProjectType
    methodology: ProjectMethodology
    phases: List[ProjectPhase]
    estimated_duration_days: Optional[int]
    estimated_budget: Optional[Decimal]
    usage_count: int
    created_at: datetime

class ProjectIntakeResponse(BaseModel):
    """Project intake form response"""
    id: str
    project_title: str
    business_justification: str
    requestor_id: str
    project_type: ProjectType
    priority: Priority
    status: ApprovalStatus
    estimated_budget: Optional[Decimal]
    requested_start_date: Optional[date]
    created_at: datetime

class ProjectSnapshotResponse(BaseModel):
    """Project snapshot response"""
    id: str
    project_id: str
    snapshot_date: datetime
    snapshot_type: str
    status: Status
    health_status: HealthStatus
    percent_complete: float
    budget_variance: Decimal
    schedule_variance_days: int
    team_size: int
    open_issues: int
    open_risks: int
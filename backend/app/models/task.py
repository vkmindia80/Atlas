from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from decimal import Decimal
from .common import BaseDocument, Priority, Status, HealthStatus
from enum import Enum

class TaskType(str, Enum):
    STORY = "story"
    TASK = "task"
    BUG = "bug"
    EPIC = "epic"
    SUBTASK = "subtask"
    MILESTONE = "milestone"

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    TESTING = "testing"
    DONE = "done"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"

class DependencyType(str, Enum):
    FINISH_TO_START = "finish_to_start"  # Task B starts after Task A finishes
    START_TO_START = "start_to_start"    # Task B starts when Task A starts
    FINISH_TO_FINISH = "finish_to_finish" # Task B finishes when Task A finishes
    START_TO_FINISH = "start_to_finish"   # Task B finishes when Task A starts

class TaskDependency(BaseModel):
    """Task dependency relationship"""
    id: str = Field(default_factory=lambda: str(__import__('uuid').uuid4()))
    predecessor_task_id: str
    successor_task_id: str
    dependency_type: DependencyType = DependencyType.FINISH_TO_START
    lag_days: int = 0  # Lag time in days (positive for delay, negative for overlap)
    is_critical_path: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TaskAssignment(BaseModel):
    """Task assignment to user"""
    user_id: str
    role: str = "assignee"
    allocation_percentage: float = Field(default=100.0, ge=0, le=100)
    assigned_at: datetime = Field(default_factory=datetime.utcnow)
    assigned_by: str

class TimeEntry(BaseModel):
    """Time tracking entry"""
    id: str = Field(default_factory=lambda: str(__import__('uuid').uuid4()))
    user_id: str
    date: date
    hours: float = Field(..., gt=0, le=24)
    description: Optional[str] = None
    is_billable: bool = True
    hourly_rate: Optional[Decimal] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Task(BaseDocument):
    """Enhanced task model with dependencies and time tracking"""
    name: str = Field(..., max_length=200)
    description: Optional[str] = None
    
    # Classification
    task_type: TaskType = TaskType.TASK
    status: TaskStatus = TaskStatus.TODO
    priority: Priority = Priority.MEDIUM
    
    # Hierarchy
    project_id: str
    parent_task_id: Optional[str] = None
    milestone_id: Optional[str] = None
    
    # Assignment
    assignments: List[TaskAssignment] = Field(default_factory=list)
    
    # Timeline
    planned_start_date: Optional[date] = None
    planned_end_date: Optional[date] = None
    actual_start_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    
    # Effort estimation
    estimated_hours: Optional[float] = None
    remaining_hours: Optional[float] = None
    
    # Progress
    percent_complete: float = Field(default=0.0, ge=0, le=100)
    
    # Dependencies
    dependencies: List[TaskDependency] = Field(default_factory=list)
    
    # Time tracking
    time_entries: List[TimeEntry] = Field(default_factory=list)
    
    # Labels and tags
    labels: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    
    # Additional fields
    story_points: Optional[int] = None
    business_value: Optional[int] = None
    
    # Kanban board position
    board_column: str = "todo"
    board_position: int = 0
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }

class TaskCreate(BaseModel):
    """Schema for creating a new task"""
    name: str = Field(..., max_length=200)
    description: Optional[str] = None
    task_type: TaskType = TaskType.TASK
    priority: Priority = Priority.MEDIUM
    project_id: str
    parent_task_id: Optional[str] = None
    milestone_id: Optional[str] = None
    planned_start_date: Optional[date] = None
    planned_end_date: Optional[date] = None
    estimated_hours: Optional[float] = None
    story_points: Optional[int] = None
    labels: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)

class TaskUpdate(BaseModel):
    """Schema for updating task"""
    name: Optional[str] = None
    description: Optional[str] = None
    task_type: Optional[TaskType] = None
    status: Optional[TaskStatus] = None
    priority: Optional[Priority] = None
    parent_task_id: Optional[str] = None
    milestone_id: Optional[str] = None
    planned_start_date: Optional[date] = None
    planned_end_date: Optional[date] = None
    actual_start_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    estimated_hours: Optional[float] = None
    remaining_hours: Optional[float] = None
    percent_complete: Optional[float] = None
    story_points: Optional[int] = None
    business_value: Optional[int] = None
    board_column: Optional[str] = None
    board_position: Optional[int] = None
    labels: Optional[List[str]] = None
    tags: Optional[List[str]] = None

class TaskResponse(BaseModel):
    """Task response model"""
    id: str
    name: str
    description: Optional[str]
    task_type: TaskType
    status: TaskStatus
    priority: Priority
    project_id: str
    parent_task_id: Optional[str]
    milestone_id: Optional[str]
    planned_start_date: Optional[date]
    planned_end_date: Optional[date]
    actual_start_date: Optional[date]
    actual_end_date: Optional[date]
    estimated_hours: Optional[float]
    remaining_hours: Optional[float]
    percent_complete: float
    story_points: Optional[int]
    business_value: Optional[int]
    board_column: str
    board_position: int
    labels: List[str]
    tags: List[str]
    assignments: List[TaskAssignment]
    dependencies: List[TaskDependency]
    total_time_logged: float = 0.0
    created_at: datetime
    updated_at: datetime

class BulkTaskUpdate(BaseModel):
    """Schema for bulk task operations"""
    task_ids: List[str]
    updates: TaskUpdate

class TaskFilter(BaseModel):
    """Task filtering options"""
    project_id: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[Priority] = None
    assignee_id: Optional[str] = None
    milestone_id: Optional[str] = None
    start_date_from: Optional[date] = None
    start_date_to: Optional[date] = None
    due_date_from: Optional[date] = None
    due_date_to: Optional[date] = None
    labels: Optional[List[str]] = None
    tags: Optional[List[str]] = None
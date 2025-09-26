from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from decimal import Decimal
from .common import BaseDocument, Priority, Status
from enum import Enum

class ObjectiveType(str, Enum):
    FINANCIAL = "financial"
    CUSTOMER = "customer"
    INTERNAL_PROCESS = "internal_process"
    LEARNING_GROWTH = "learning_growth"
    STRATEGIC_INITIATIVE = "strategic_initiative"

class MeasurementUnit(str, Enum):
    PERCENTAGE = "percentage"
    CURRENCY = "currency"
    COUNT = "count"
    DAYS = "days"
    SCORE = "score"
    RATIO = "ratio"

class KPI(BaseModel):
    """Key Performance Indicator model"""
    id: str = Field(default_factory=lambda: str(__import__('uuid').uuid4()))
    name: str
    description: Optional[str] = None
    measurement_unit: MeasurementUnit
    target_value: float
    current_value: float = 0.0
    baseline_value: Optional[float] = None
    threshold_red: Optional[float] = None
    threshold_yellow: Optional[float] = None
    threshold_green: Optional[float] = None
    is_higher_better: bool = True  # Direction of improvement

class StrategicObjective(BaseDocument):
    """Strategic Objective model for portfolio alignment"""
    name: str = Field(..., max_length=200)
    code: str = Field(..., max_length=50)  # Unique within tenant
    description: Optional[str] = None
    
    # Classification
    objective_type: ObjectiveType
    status: Status = Status.ACTIVE
    priority: Priority = Priority.MEDIUM
    
    # Ownership
    owner_id: str  # User ID responsible for this objective
    stakeholders: List[str] = Field(default_factory=list)  # User IDs
    
    # Timeline
    start_date: Optional[date] = None
    target_date: Optional[date] = None
    
    # Metrics and KPIs
    kpis: List[KPI] = Field(default_factory=list)
    
    # Relationships
    parent_objective_id: Optional[str] = None  # For objective hierarchy
    child_objective_ids: List[str] = Field(default_factory=list)
    
    # Strategic context
    business_case: Optional[str] = None
    success_criteria: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    
    # Financial impact
    investment_required: Optional[Decimal] = None
    expected_benefit: Optional[Decimal] = None
    payback_period_months: Optional[int] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }

class StrategicObjectiveCreate(BaseModel):
    """Schema for creating a strategic objective"""
    name: str = Field(..., max_length=200)
    code: str = Field(..., max_length=50)
    description: Optional[str] = None
    objective_type: ObjectiveType
    priority: Priority = Priority.MEDIUM
    owner_id: str
    stakeholders: List[str] = Field(default_factory=list)
    start_date: Optional[date] = None
    target_date: Optional[date] = None
    parent_objective_id: Optional[str] = None
    success_criteria: List[str] = Field(default_factory=list)

class StrategicObjectiveUpdate(BaseModel):
    """Schema for updating strategic objective"""
    name: Optional[str] = None
    description: Optional[str] = None
    objective_type: Optional[ObjectiveType] = None
    status: Optional[Status] = None
    priority: Optional[Priority] = None
    owner_id: Optional[str] = None
    stakeholders: Optional[List[str]] = None
    start_date: Optional[date] = None
    target_date: Optional[date] = None
    success_criteria: Optional[List[str]] = None

class StrategicObjectiveResponse(BaseModel):
    """Strategic objective response model"""
    id: str
    name: str
    code: str
    description: Optional[str]
    objective_type: ObjectiveType
    status: Status
    priority: Priority
    owner_id: str
    stakeholders: List[str]
    start_date: Optional[date]
    target_date: Optional[date]
    kpis: List[KPI]
    parent_objective_id: Optional[str]
    child_objective_ids: List[str]
    created_at: datetime
    updated_at: datetime
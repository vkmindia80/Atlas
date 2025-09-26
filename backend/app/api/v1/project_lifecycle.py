from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.security import HTTPBearer
from typing import List, Optional, Dict, Any
import csv
import io
from ...core.database import get_database
from ...core.middleware import get_current_user_and_tenant
from ...models.project_enhanced import (
    ProjectTemplate, ProjectIntakeForm, ProjectBaseline, ProjectApproval, 
    ProjectSnapshot, ProjectEnhanced, ProjectTemplateResponse, 
    ProjectIntakeResponse, ProjectSnapshotResponse,
    ProjectPhase, ApprovalStatus
)
from ...models.user import UserRole
from ...utils.rbac import Permission, user_has_permission
from datetime import datetime, date
import uuid
import json

router = APIRouter()
security = HTTPBearer()

async def get_current_user_with_permissions(credentials = Depends(security)):
    """Get current user with permission checking"""
    return await get_current_user_and_tenant(credentials)

# Project Templates
@router.post("/project-templates", response_model=ProjectTemplateResponse)
async def create_project_template(
    template_data: dict,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """Create a new project template"""
    if not user_has_permission(UserRole(current_user["user_role"]), Permission.CREATE_PROJECT):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to create project template"
        )
    
    db = await get_database()
    templates_collection = db.get_default_database().project_templates
    
    # Create template document
    template_id = str(uuid.uuid4())
    template_doc = {
        "_id": template_id,
        "tenant_id": current_user["tenant_id"],
        "name": template_data["name"],
        "description": template_data.get("description"),
        "project_type": template_data["project_type"],
        "methodology": template_data["methodology"],
        "phases": template_data.get("phases", []),
        "default_milestones": template_data.get("default_milestones", []),
        "task_templates": template_data.get("task_templates", []),
        "estimated_duration_days": template_data.get("estimated_duration_days"),
        "estimated_budget": template_data.get("estimated_budget", 0),
        "required_skills": template_data.get("required_skills", []),
        "usage_count": 0,
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "created_by": current_user["user_id"],
        "metadata": {}
    }
    
    await templates_collection.insert_one(template_doc)
    
    return ProjectTemplateResponse(
        id=template_doc["_id"],
        name=template_doc["name"],
        description=template_doc["description"],
        project_type=template_doc["project_type"],
        methodology=template_doc["methodology"],
        phases=[ProjectPhase(**phase) for phase in template_doc["phases"]],
        estimated_duration_days=template_doc["estimated_duration_days"],
        estimated_budget=template_doc["estimated_budget"],
        usage_count=template_doc["usage_count"],
        created_at=template_doc["created_at"]
    )

@router.get("/project-templates", response_model=List[ProjectTemplateResponse])
async def list_project_templates(
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """List available project templates"""
    db = await get_database()
    templates_collection = db.get_default_database().project_templates
    
    templates = await templates_collection.find({
        "tenant_id": current_user["tenant_id"],
        "is_active": True
    }).to_list(length=None)
    
    return [
        ProjectTemplateResponse(
            id=template["_id"],
            name=template["name"],
            description=template["description"],
            project_type=template["project_type"],
            methodology=template["methodology"],
            phases=[ProjectPhase(**phase) for phase in template["phases"]],
            estimated_duration_days=template["estimated_duration_days"],
            estimated_budget=template["estimated_budget"],
            usage_count=template["usage_count"],
            created_at=template["created_at"]
        )
        for template in templates
    ]

# Project Intake Forms
@router.post("/project-intake", response_model=ProjectIntakeResponse)
async def create_project_intake(
    intake_data: dict,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """Submit a new project intake form"""
    db = await get_database()
    intake_collection = db.get_default_database().project_intake_forms
    
    # Create intake form
    intake_id = str(uuid.uuid4())
    intake_doc = {
        "_id": intake_id,
        "tenant_id": current_user["tenant_id"],
        "project_title": intake_data["project_title"],
        "business_justification": intake_data["business_justification"],
        "project_description": intake_data["project_description"],
        "expected_benefits": intake_data["expected_benefits"],
        "requestor_id": current_user["user_id"],
        "requestor_department": intake_data["requestor_department"],
        "sponsor_id": intake_data.get("sponsor_id"),
        "project_type": intake_data["project_type"],
        "priority": intake_data["priority"],
        "requested_start_date": intake_data.get("requested_start_date"),
        "requested_end_date": intake_data.get("requested_end_date"),
        "estimated_budget": intake_data.get("estimated_budget", 0),
        "functional_requirements": intake_data.get("functional_requirements", []),
        "non_functional_requirements": intake_data.get("non_functional_requirements", []),
        "constraints": intake_data.get("constraints", []),
        "assumptions": intake_data.get("assumptions", []),
        "required_skills": intake_data.get("required_skills", []),
        "estimated_team_size": intake_data.get("estimated_team_size"),
        "identified_risks": intake_data.get("identified_risks", []),
        "risk_level": intake_data.get("risk_level", "medium"),
        "status": ApprovalStatus.PENDING,
        "approvals": [],
        "decision_date": None,
        "decision_notes": None,
        "approved_budget": None,
        "assigned_pm": None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "created_by": current_user["user_id"],
        "is_active": True,
        "metadata": {}
    }
    
    await intake_collection.insert_one(intake_doc)
    
    return ProjectIntakeResponse(
        id=intake_doc["_id"],
        project_title=intake_doc["project_title"],
        business_justification=intake_doc["business_justification"],
        requestor_id=intake_doc["requestor_id"],
        project_type=intake_doc["project_type"],
        priority=intake_doc["priority"],
        status=ApprovalStatus(intake_doc["status"]),
        estimated_budget=intake_doc["estimated_budget"],
        requested_start_date=intake_doc["requested_start_date"],
        created_at=intake_doc["created_at"]
    )

@router.get("/project-intake", response_model=List[ProjectIntakeResponse])
async def list_project_intakes(
    status: Optional[ApprovalStatus] = None,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """List project intake forms"""
    db = await get_database()
    intake_collection = db.get_default_database().project_intake_forms
    
    filter_query = {"tenant_id": current_user["tenant_id"], "is_active": True}
    if status:
        filter_query["status"] = status
    
    intakes = await intake_collection.find(filter_query).to_list(length=None)
    
    return [
        ProjectIntakeResponse(
            id=intake["_id"],
            project_title=intake["project_title"],
            business_justification=intake["business_justification"],
            requestor_id=intake["requestor_id"],
            project_type=intake["project_type"],
            priority=intake["priority"],
            status=ApprovalStatus(intake["status"]),
            estimated_budget=intake["estimated_budget"],
            requested_start_date=intake["requested_start_date"],
            created_at=intake["created_at"]
        )
        for intake in intakes
    ]

# Project Baselines
@router.post("/projects/{project_id}/baseline")
async def create_project_baseline(
    project_id: str,
    baseline_data: dict,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """Create a new project baseline"""
    db = await get_database()
    projects_collection = db.get_default_database().projects
    
    # Verify project exists
    project = await projects_collection.find_one({
        "_id": project_id,
        "tenant_id": current_user["tenant_id"],
        "is_active": True
    })
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Create baseline
    baseline = ProjectBaseline(
        name=baseline_data["name"],
        description=baseline_data.get("description"),
        created_by=current_user["user_id"],
        planned_start_date=baseline_data.get("planned_start_date"),
        planned_end_date=baseline_data.get("planned_end_date"),
        total_budget=baseline_data.get("total_budget", 0),
        scope_description=baseline_data.get("scope_description"),
        key_milestones=baseline_data.get("key_milestones", []),
        is_current_baseline=baseline_data.get("is_current_baseline", False)
    )
    
    # Update project with baseline
    await projects_collection.update_one(
        {"_id": project_id},
        {
            "$push": {"baselines": baseline.dict()},
            "$set": {
                "current_baseline_id": baseline.id if baseline.is_current_baseline else project.get("current_baseline_id"),
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    return {"message": "Baseline created successfully", "baseline_id": baseline.id}

# Project Snapshots
@router.post("/projects/{project_id}/snapshot")
async def create_project_snapshot(
    project_id: str,
    snapshot_data: dict,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """Create a project snapshot"""
    db = await get_database()
    snapshots_collection = db.get_default_database().project_snapshots
    projects_collection = db.get_default_database().projects
    tasks_collection = db.get_default_database().tasks
    
    # Get project data
    project = await projects_collection.find_one({
        "_id": project_id,
        "tenant_id": current_user["tenant_id"],
        "is_active": True
    })
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Calculate metrics
    tasks = await tasks_collection.find({
        "project_id": project_id,
        "tenant_id": current_user["tenant_id"],
        "is_active": True
    }).to_list(length=None)
    
    completed_tasks = len([t for t in tasks if t["status"] == "done"])
    
    # Create snapshot document
    snapshot_id = str(uuid.uuid4())
    snapshot_doc = {
        "_id": snapshot_id,
        "tenant_id": current_user["tenant_id"],
        "project_id": project_id,
        "snapshot_date": datetime.utcnow(),
        "snapshot_type": snapshot_data.get("snapshot_type", "ad_hoc"),
        "status": project["status"],
        "health_status": project["health_status"],
        "percent_complete": project["percent_complete"],
        "budget_spent": project["financials"]["spent_amount"],
        "budget_committed": project["financials"]["committed_amount"],
        "budget_variance": project["financials"]["budget_variance"],
        "schedule_variance_days": 0,  # Calculate based on planned vs actual
        "critical_path_delay": 0,
        "team_size": len(project["team_members"]),
        "team_utilization": 0.0,  # Calculate from time entries
        "tasks_completed": completed_tasks,
        "tasks_remaining": len(tasks) - completed_tasks,
        "milestones_completed": len([m for m in project.get("milestones", []) if m.get("status") == "completed"]),
        "milestones_remaining": len([m for m in project.get("milestones", []) if m.get("status") != "completed"]),
        "open_issues": project["open_issues_count"],
        "open_risks": project["open_risks_count"],
        "risk_score": project["risk_score"],
        "status_notes": snapshot_data.get("status_notes"),
        "achievements": snapshot_data.get("achievements", []),
        "challenges": snapshot_data.get("challenges", []),
        "next_period_plans": snapshot_data.get("next_period_plans", []),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "created_by": current_user["user_id"],
        "is_active": True,
        "metadata": {}
    }
    
    await snapshots_collection.insert_one(snapshot_doc)
    
    return ProjectSnapshotResponse(
        id=snapshot_doc["_id"],
        project_id=snapshot_doc["project_id"],
        snapshot_date=snapshot_doc["snapshot_date"],
        snapshot_type=snapshot_doc["snapshot_type"],
        status=snapshot_doc["status"],
        health_status=snapshot_doc["health_status"],
        percent_complete=snapshot_doc["percent_complete"],
        budget_variance=snapshot_doc["budget_variance"],
        schedule_variance_days=snapshot_doc["schedule_variance_days"],
        team_size=snapshot_doc["team_size"],
        open_issues=snapshot_doc["open_issues"],
        open_risks=snapshot_doc["open_risks"]
    )

@router.get("/projects/{project_id}/snapshots", response_model=List[ProjectSnapshotResponse])
async def list_project_snapshots(
    project_id: str,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """List project snapshots"""
    db = await get_database()
    snapshots_collection = db.get_default_database().project_snapshots
    
    snapshots = await snapshots_collection.find({
        "project_id": project_id,
        "tenant_id": current_user["tenant_id"],
        "is_active": True
    }).sort("snapshot_date", -1).to_list(length=None)
    
    return [
        ProjectSnapshotResponse(
            id=snapshot["_id"],
            project_id=snapshot["project_id"],
            snapshot_date=snapshot["snapshot_date"],
            snapshot_type=snapshot["snapshot_type"],
            status=snapshot["status"],
            health_status=snapshot["health_status"],
            percent_complete=snapshot["percent_complete"],
            budget_variance=snapshot["budget_variance"],
            schedule_variance_days=snapshot["schedule_variance_days"],
            team_size=snapshot["team_size"],
            open_issues=snapshot["open_issues"],
            open_risks=snapshot["open_risks"]
        )
        for snapshot in snapshots
    ]

# CSV Import
@router.post("/projects/import-csv")
async def import_projects_csv(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """Import projects from CSV file"""
    if not user_has_permission(UserRole(current_user["user_role"]), Permission.CREATE_PROJECT):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to import projects"
        )
    
    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be a CSV"
        )
    
    # Read CSV content
    content = await file.read()
    csv_content = content.decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(csv_content))
    
    db = await get_database()
    projects_collection = db.get_default_database().projects
    
    imported_projects = []
    errors = []
    
    for row_num, row in enumerate(csv_reader, 1):
        try:
            # Validate required fields
            if not row.get('name') or not row.get('code'):
                errors.append(f"Row {row_num}: Missing required fields (name, code)")
                continue
            
            # Check if project code already exists
            existing = await projects_collection.find_one({
                "code": row['code'],
                "tenant_id": current_user["tenant_id"]
            })
            
            if existing:
                errors.append(f"Row {row_num}: Project code '{row['code']}' already exists")
                continue
            
            # Create project document
            project_id = str(uuid.uuid4())
            project_doc = {
                "_id": project_id,
                "tenant_id": current_user["tenant_id"],
                "name": row['name'],
                "code": row['code'],
                "description": row.get('description', ''),
                "project_type": row.get('project_type', 'other'),
                "methodology": row.get('methodology', 'agile'),
                "status": row.get('status', 'draft'),
                "health_status": "green",
                "priority": row.get('priority', 'medium'),
                "portfolio_id": row.get('portfolio_id'),
                "parent_project_id": row.get('parent_project_id'),
                "project_manager_id": row.get('project_manager_id', current_user["user_id"]),
                "sponsor_id": row.get('sponsor_id'),
                "team_members": [],
                "planned_start_date": row.get('planned_start_date'),
                "planned_end_date": row.get('planned_end_date'),
                "actual_start_date": None,
                "actual_end_date": None,
                "percent_complete": float(row.get('percent_complete', 0)),
                "milestones": [],
                "financials": {
                    "total_budget": float(row.get('total_budget', 0)),
                    "allocated_budget": 0,
                    "spent_amount": 0,
                    "committed_amount": 0,
                    "forecasted_cost": 0,
                    "budget_variance": 0,
                    "cost_to_complete": 0,
                    "labor_cost": 0,
                    "material_cost": 0,
                    "vendor_cost": 0,
                    "overhead_cost": 0
                },
                "resource_allocations": [],
                "risk_score": 0.0,
                "open_issues_count": 0,
                "open_risks_count": 0,
                "document_urls": [],
                "custom_fields": {},
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "created_by": current_user["user_id"],
                "is_active": True,
                "metadata": {}
            }
            
            await projects_collection.insert_one(project_doc)
            imported_projects.append(project_id)
            
        except Exception as e:
            errors.append(f"Row {row_num}: {str(e)}")
    
    return {
        "imported_count": len(imported_projects),
        "error_count": len(errors),
        "imported_project_ids": imported_projects,
        "errors": errors
    }
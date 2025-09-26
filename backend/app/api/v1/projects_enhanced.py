from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import List, Optional, Dict, Any
from datetime import date, datetime
import io
import csv
import json
from decimal import Decimal

from ...models.project_enhanced import (
    EnhancedProject, ProjectTask, ProjectIssue, ProjectRisk, ProjectApproval,
    ProjectBaseline, ProjectTemplate, ProjectIntakeForm, ProjectCreateFromIntake,
    ProjectPhase, ApprovalStatus, TaskStatus, IssueType, RiskLevel
)
from ...models.project import ProjectResponse, ProjectCreate, ProjectUpdate
from ...models.common import Status, Priority
from ...core.database import get_database
from ...core.security import get_current_user
from ...models.user import User

router = APIRouter()

@router.get("/", response_model=List[ProjectResponse])
async def get_projects(
    skip: int = 0,
    limit: int = 100,
    status: Optional[Status] = None,
    portfolio_id: Optional[str] = None,
    project_manager_id: Optional[str] = None,
    project_type: Optional[str] = None,
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Get all projects with filtering"""
    query = {"tenant_id": current_user.tenant_id, "is_active": True}
    
    if status:
        query["status"] = status
    if portfolio_id:
        query["portfolio_id"] = portfolio_id
    if project_manager_id:
        query["project_manager_id"] = project_manager_id
    if project_type:
        query["project_type"] = project_type
    
    projects = await db.projects.find(query).skip(skip).limit(limit).to_list(None)
    
    return [
        ProjectResponse(
            **project,
            team_size=len(project.get("team_members", []))
        )
        for project in projects
    ]

@router.post("/", response_model=ProjectResponse)
async def create_project(
    project_data: ProjectCreate,
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Create a new project"""
    # Check if project code is unique within tenant
    existing = await db.projects.find_one({
        "tenant_id": current_user.tenant_id,
        "code": project_data.code,
        "is_active": True
    })
    if existing:
        raise HTTPException(status_code=400, detail="Project code already exists")
    
    project = EnhancedProject(
        **project_data.dict(),
        tenant_id=current_user.tenant_id,
        created_by=current_user.id,
        current_phase=ProjectPhase.INITIATION
    )
    
    result = await db.projects.insert_one(project.dict(by_alias=True))
    project.id = result.inserted_id
    
    return ProjectResponse(**project.dict(), team_size=len(project.team_members))

@router.get("/{project_id}", response_model=Dict[str, Any])
async def get_project_detail(
    project_id: str,
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Get detailed project information with all related data"""
    project = await db.projects.find_one({
        "id": project_id,
        "tenant_id": current_user.tenant_id,
        "is_active": True
    })
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Get related data
    tasks = project.get("tasks", [])
    milestones = project.get("milestones", [])
    risks = project.get("risks", [])
    issues = project.get("issues", [])
    dependencies = project.get("dependencies", [])
    approvals = project.get("approvals", [])
    baselines = project.get("baselines", [])
    
    return {
        "project": ProjectResponse(**project, team_size=len(project.get("team_members", []))),
        "tasks": tasks,
        "milestones": milestones,
        "risks": risks,
        "issues": issues,
        "dependencies": dependencies,
        "approvals": approvals,
        "baselines": baselines,
        "task_summary": {
            "total": len(tasks),
            "not_started": len([t for t in tasks if t.get("status") == "not_started"]),
            "in_progress": len([t for t in tasks if t.get("status") == "in_progress"]),
            "completed": len([t for t in tasks if t.get("status") == "completed"]),
            "on_hold": len([t for t in tasks if t.get("status") == "on_hold"])
        }
    }

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Update project"""
    project = await db.projects.find_one({
        "id": project_id,
        "tenant_id": current_user.tenant_id,
        "is_active": True
    })
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    update_data = {k: v for k, v in project_data.dict().items() if v is not None}
    update_data["updated_by"] = current_user.id
    update_data["updated_at"] = datetime.utcnow()
    
    await db.projects.update_one(
        {"id": project_id, "tenant_id": current_user.tenant_id},
        {"$set": update_data}
    )
    
    updated_project = await db.projects.find_one({
        "id": project_id,
        "tenant_id": current_user.tenant_id
    })
    
    return ProjectResponse(**updated_project, team_size=len(updated_project.get("team_members", [])))

@router.post("/{project_id}/tasks")
async def create_task(
    project_id: str,
    task_data: Dict[str, Any],
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Create a new task in project"""
    project = await db.projects.find_one({
        "id": project_id,
        "tenant_id": current_user.tenant_id,
        "is_active": True
    })
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    task = ProjectTask(**task_data)
    
    await db.projects.update_one(
        {"id": project_id, "tenant_id": current_user.tenant_id},
        {"$push": {"tasks": task.dict()}}
    )
    
    return {"message": "Task created successfully", "task_id": task.id}

@router.put("/{project_id}/tasks/{task_id}")
async def update_task(
    project_id: str,
    task_id: str,
    task_data: Dict[str, Any],
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Update task in project"""
    update_fields = {}
    for key, value in task_data.items():
        update_fields[f"tasks.$.{key}"] = value
    
    result = await db.projects.update_one(
        {
            "id": project_id,
            "tenant_id": current_user.tenant_id,
            "tasks.id": task_id
        },
        {"$set": update_fields}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Project or task not found")
    
    return {"message": "Task updated successfully"}

@router.delete("/{project_id}/tasks/{task_id}")
async def delete_task(
    project_id: str,
    task_id: str,
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Delete task from project"""
    result = await db.projects.update_one(
        {"id": project_id, "tenant_id": current_user.tenant_id},
        {"$pull": {"tasks": {"id": task_id}}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {"message": "Task deleted successfully"}

@router.post("/{project_id}/issues")
async def create_issue(
    project_id: str,
    issue_data: Dict[str, Any],
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Create project issue"""
    project = await db.projects.find_one({
        "id": project_id,
        "tenant_id": current_user.tenant_id,
        "is_active": True
    })
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    issue = ProjectIssue(
        reporter_id=current_user.id,
        **issue_data
    )
    
    await db.projects.update_one(
        {"id": project_id, "tenant_id": current_user.tenant_id},
        {
            "$push": {"issues": issue.dict()},
            "$inc": {"open_issues_count": 1}
        }
    )
    
    return {"message": "Issue created successfully", "issue_id": issue.id}

@router.post("/{project_id}/risks")
async def create_risk(
    project_id: str,
    risk_data: Dict[str, Any],
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Create project risk"""
    project = await db.projects.find_one({
        "id": project_id,
        "tenant_id": current_user.tenant_id,
        "is_active": True
    })
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    risk = ProjectRisk(
        owner_id=current_user.id,
        identified_by=current_user.id,
        **risk_data
    )
    
    # Calculate risk score (probability * impact)
    risk_score = risk.probability * risk.impact
    
    await db.projects.update_one(
        {"id": project_id, "tenant_id": current_user.tenant_id},
        {
            "$push": {"risks": risk.dict()},
            "$inc": {"open_risks_count": 1},
            "$max": {"risk_score": risk_score}
        }
    )
    
    return {"message": "Risk created successfully", "risk_id": risk.id}

@router.post("/{project_id}/baselines")
async def create_baseline(
    project_id: str,
    baseline_data: Dict[str, Any],
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Create project baseline snapshot"""
    project = await db.projects.find_one({
        "id": project_id,
        "tenant_id": current_user.tenant_id,
        "is_active": True
    })
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    baseline = ProjectBaseline(
        created_by=current_user.id,
        planned_start_date=project.get("planned_start_date"),
        planned_end_date=project.get("planned_end_date"),
        total_budget=project.get("financials", {}).get("total_budget", 0),
        milestones_snapshot=project.get("milestones", []),
        tasks_snapshot=project.get("tasks", []),
        resource_snapshot=project.get("resource_allocations", []),
        **baseline_data
    )
    
    await db.projects.update_one(
        {"id": project_id, "tenant_id": current_user.tenant_id},
        {
            "$push": {"baselines": baseline.dict()},
            "$set": {"current_baseline_id": baseline.id}
        }
    )
    
    return {"message": "Baseline created successfully", "baseline_id": baseline.id}

@router.post("/{project_id}/approvals")
async def request_approval(
    project_id: str,
    approval_data: Dict[str, Any],
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Request project approval"""
    project = await db.projects.find_one({
        "id": project_id,
        "tenant_id": current_user.tenant_id,
        "is_active": True
    })
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    approval = ProjectApproval(
        requested_by=current_user.id,
        **approval_data
    )
    
    await db.projects.update_one(
        {"id": project_id, "tenant_id": current_user.tenant_id},
        {"$push": {"approvals": approval.dict()}}
    )
    
    return {"message": "Approval requested successfully", "approval_id": approval.id}

@router.put("/{project_id}/approvals/{approval_id}")
async def process_approval(
    project_id: str,
    approval_id: str,
    approval_decision: Dict[str, Any],
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Process approval (approve/reject)"""
    update_fields = {
        f"approvals.$.status": approval_decision["status"],
        f"approvals.$.approval_date": datetime.utcnow(),
        f"approvals.$.approval_comments": approval_decision.get("comments", "")
    }
    
    result = await db.projects.update_one(
        {
            "id": project_id,
            "tenant_id": current_user.tenant_id,
            "approvals.id": approval_id,
            "approvals.$.approver_id": current_user.id
        },
        {"$set": update_fields}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Approval not found or unauthorized")
    
    # If this is a baseline approval, update project status
    if approval_decision["status"] == "approved":
        project = await db.projects.find_one({"id": project_id})
        approvals = project.get("approvals", [])
        for approval in approvals:
            if approval["id"] == approval_id and approval["approval_type"] == "baseline":
                await db.projects.update_one(
                    {"id": project_id},
                    {"$set": {"status": "active", "current_phase": "execution"}}
                )
                break
    
    return {"message": "Approval processed successfully"}

@router.post("/bulk-update-status")
async def bulk_update_project_status(
    updates: List[Dict[str, Any]],
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Bulk update project statuses"""
    results = []
    
    for update in updates:
        project_id = update["project_id"]
        new_status = update["status"]
        
        result = await db.projects.update_one(
            {"id": project_id, "tenant_id": current_user.tenant_id},
            {
                "$set": {
                    "status": new_status,
                    "updated_by": current_user.id,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        results.append({
            "project_id": project_id,
            "success": result.matched_count > 0,
            "new_status": new_status if result.matched_count > 0 else None
        })
    
    return {"results": results}

@router.post("/import-csv")
async def import_projects_csv(
    file: UploadFile = File(...),
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Import projects from CSV file"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be CSV format")
    
    content = await file.read()
    csv_data = content.decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(csv_data))
    
    imported_projects = []
    errors = []
    
    for row_num, row in enumerate(csv_reader, start=2):
        try:
            # Validate required fields
            required_fields = ['name', 'code', 'project_type', 'project_manager_id']
            for field in required_fields:
                if not row.get(field):
                    raise ValueError(f"Missing required field: {field}")
            
            # Check for duplicate code
            existing = await db.projects.find_one({
                "tenant_id": current_user.tenant_id,
                "code": row["code"],
                "is_active": True
            })
            if existing:
                raise ValueError(f"Project code {row['code']} already exists")
            
            # Create project
            project_data = {
                "name": row["name"],
                "code": row["code"],
                "description": row.get("description", ""),
                "project_type": row["project_type"],
                "project_manager_id": row["project_manager_id"],
                "priority": row.get("priority", "medium"),
                "planned_start_date": row.get("planned_start_date"),
                "planned_end_date": row.get("planned_end_date")
            }
            
            project = EnhancedProject(
                **project_data,
                tenant_id=current_user.tenant_id,
                created_by=current_user.id
            )
            
            result = await db.projects.insert_one(project.dict(by_alias=True))
            imported_projects.append({
                "row": row_num,
                "project_id": str(result.inserted_id),
                "name": project.name,
                "code": project.code
            })
            
        except Exception as e:
            errors.append({
                "row": row_num,
                "error": str(e),
                "data": row
            })
    
    return {
        "success_count": len(imported_projects),
        "error_count": len(errors),
        "imported_projects": imported_projects,
        "errors": errors
    }

# Project Templates
@router.get("/templates/", response_model=List[Dict[str, Any]])
async def get_project_templates(
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Get project templates"""
    templates = await db.project_templates.find({
        "tenant_id": current_user.tenant_id,
        "is_active": True
    }).to_list(None)
    
    return templates

@router.post("/templates/")
async def create_project_template(
    template_data: Dict[str, Any],
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Create project template"""
    template = ProjectTemplate(
        **template_data,
        created_by=current_user.id,
        tenant_id=current_user.tenant_id
    )
    
    await db.project_templates.insert_one(template.dict())
    
    return {"message": "Template created successfully", "template_id": template.id}

@router.post("/from-intake")
async def create_project_from_intake(
    intake_data: ProjectCreateFromIntake,
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Create project from intake form"""
    intake = intake_data.intake_data
    
    # Check if project code/name is unique
    existing = await db.projects.find_one({
        "tenant_id": current_user.tenant_id,
        "name": intake.project_name,
        "is_active": True
    })
    if existing:
        raise HTTPException(status_code=400, detail="Project name already exists")
    
    # Create project from intake
    project_data = {
        "name": intake.project_name,
        "code": intake.project_name.upper().replace(" ", "_"),
        "description": intake.business_justification,
        "project_type": intake.project_type,
        "methodology": intake.methodology,
        "priority": intake.priority,
        "sponsor_id": intake.project_sponsor,
        "project_manager_id": intake.preferred_project_manager or current_user.id,
        "planned_start_date": intake.requested_start_date,
        "planned_end_date": intake.target_end_date,
        "portfolio_id": intake.portfolio_id,
        "custom_fields": {
            "intake_form": intake.dict(),
            "business_case_url": intake.business_case_url,
            "success_criteria": intake.success_criteria
        }
    }
    
    # Apply template if specified
    if intake_data.template_id:
        template = await db.project_templates.find_one({
            "id": intake_data.template_id,
            "tenant_id": current_user.tenant_id
        })
        if template:
            project_data.update({
                "template_id": intake_data.template_id,
                "tasks": template.get("template_tasks", []),
                "milestones": template.get("template_milestones", [])
            })
    
    project = EnhancedProject(
        **project_data,
        tenant_id=current_user.tenant_id,
        created_by=current_user.id,
        requires_approval=not intake_data.auto_approve
    )
    
    result = await db.projects.insert_one(project.dict(by_alias=True))
    project.id = result.inserted_id
    
    # Create approval request if required
    if project.requires_approval and not intake_data.auto_approve:
        approval = ProjectApproval(
            approval_type="initiation",
            description="Project initiation approval",
            justification=intake.business_justification,
            requested_by=current_user.id,
            approver_id=intake.project_sponsor
        )
        
        await db.projects.update_one(
            {"id": project.id},
            {"$push": {"approvals": approval.dict()}}
        )
    
    return {
        "message": "Project created from intake successfully",
        "project_id": project.id,
        "requires_approval": project.requires_approval
    }
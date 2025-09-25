from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer
from typing import List, Optional
from ...core.database import get_database
from ...core.middleware import get_current_user_and_tenant
from ...models.project import (
    ProjectCreate, ProjectUpdate, ProjectResponse, 
    Project, ProjectType, ProjectMethodology, Priority, Status
)
from ...models.user import UserRole
from ...utils.rbac import Permission, user_has_permission, get_resource_access_level, AccessLevel
from datetime import datetime
import uuid

router = APIRouter()
security = HTTPBearer()

async def get_current_user_with_permissions(credentials = Depends(security)):
    """Get current user with permission checking"""
    return await get_current_user_and_tenant(credentials)

@router.post("/projects", response_model=ProjectResponse)
async def create_project(
    project_data: ProjectCreate,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """Create a new project"""
    # Check permissions
    if not user_has_permission(UserRole(current_user["user_role"]), Permission.CREATE_PROJECT):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to create project"
        )
    
    db = await get_database()
    projects_collection = db.get_default_database().projects
    portfolios_collection = db.get_default_database().portfolios
    
    # Check if project code already exists in tenant
    existing_project = await projects_collection.find_one({
        "code": project_data.code,
        "tenant_id": current_user["tenant_id"]
    })
    
    if existing_project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project code already exists"
        )
    
    # Verify portfolio exists if specified
    if project_data.portfolio_id:
        portfolio = await portfolios_collection.find_one({
            "_id": project_data.portfolio_id,
            "tenant_id": current_user["tenant_id"]
        })
        if not portfolio:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Portfolio not found"
            )
    
    # Create project document
    project_id = str(uuid.uuid4())
    project_doc = {
        "_id": project_id,
        "tenant_id": current_user["tenant_id"],
        "name": project_data.name,
        "code": project_data.code,
        "description": project_data.description,
        "project_type": project_data.project_type,
        "methodology": project_data.methodology,
        "status": Status.DRAFT,
        "health_status": "green",
        "priority": project_data.priority,
        "portfolio_id": project_data.portfolio_id,
        "parent_project_id": project_data.parent_project_id,
        "project_manager_id": project_data.project_manager_id,
        "sponsor_id": project_data.sponsor_id,
        "team_members": [],
        "planned_start_date": project_data.planned_start_date,
        "planned_end_date": project_data.planned_end_date,
        "actual_start_date": None,
        "actual_end_date": None,
        "percent_complete": 0.0,
        "milestones": [],
        "financials": {
            "total_budget": 0,
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
    
    # Insert project
    await projects_collection.insert_one(project_doc)
    
    # Update portfolio if specified
    if project_data.portfolio_id:
        await portfolios_collection.update_one(
            {"_id": project_data.portfolio_id},
            {"$push": {"project_ids": project_id}}
        )
    
    return ProjectResponse(
        id=project_doc["_id"],
        name=project_doc["name"],
        code=project_doc["code"],
        description=project_doc["description"],
        project_type=project_doc["project_type"],
        methodology=project_doc["methodology"],
        status=project_doc["status"],
        health_status=project_doc["health_status"],
        priority=project_doc["priority"],
        portfolio_id=project_doc["portfolio_id"],
        project_manager_id=project_doc["project_manager_id"],
        sponsor_id=project_doc["sponsor_id"],
        planned_start_date=project_doc["planned_start_date"],
        planned_end_date=project_doc["planned_end_date"],
        actual_start_date=project_doc["actual_start_date"],
        actual_end_date=project_doc["actual_end_date"],
        percent_complete=project_doc["percent_complete"],
        financials=project_doc["financials"],
        risk_score=project_doc["risk_score"],
        open_issues_count=project_doc["open_issues_count"],
        open_risks_count=project_doc["open_risks_count"],
        team_size=len(project_doc["team_members"]),
        created_at=project_doc["created_at"],
        updated_at=project_doc["updated_at"]
    )

@router.get("/projects", response_model=List[ProjectResponse])
async def list_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    portfolio_id: Optional[str] = None,
    project_type: Optional[ProjectType] = None,
    status: Optional[Status] = None,
    priority: Optional[Priority] = None,
    project_manager_id: Optional[str] = None,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """List projects with optional filtering"""
    # Check permissions
    if not user_has_permission(UserRole(current_user["user_role"]), Permission.VIEW_PROJECT):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to view projects"
        )
    
    db = await get_database()
    projects_collection = db.get_default_database().projects
    
    # Build filter query
    filter_query = {"tenant_id": current_user["tenant_id"], "is_active": True}
    
    if portfolio_id:
        filter_query["portfolio_id"] = portfolio_id
    if project_type:
        filter_query["project_type"] = project_type
    if status:
        filter_query["status"] = status
    if priority:
        filter_query["priority"] = priority
    if project_manager_id:
        filter_query["project_manager_id"] = project_manager_id
    
    # Execute query
    cursor = projects_collection.find(filter_query).skip(skip).limit(limit)
    projects = await cursor.to_list(length=limit)
    
    return [
        ProjectResponse(
            id=project["_id"],
            name=project["name"],
            code=project["code"],
            description=project["description"],
            project_type=project["project_type"],
            methodology=project["methodology"],
            status=project["status"],
            health_status=project["health_status"],
            priority=project["priority"],
            portfolio_id=project["portfolio_id"],
            project_manager_id=project["project_manager_id"],
            sponsor_id=project["sponsor_id"],
            planned_start_date=project["planned_start_date"],
            planned_end_date=project["planned_end_date"],
            actual_start_date=project["actual_start_date"],
            actual_end_date=project["actual_end_date"],
            percent_complete=project["percent_complete"],
            financials=project["financials"],
            risk_score=project["risk_score"],
            open_issues_count=project["open_issues_count"],
            open_risks_count=project["open_risks_count"],
            team_size=len(project["team_members"]),
            created_at=project["created_at"],
            updated_at=project["updated_at"]
        )
        for project in projects
    ]

@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """Get project by ID"""
    db = await get_database()
    projects_collection = db.get_default_database().projects
    
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
    
    # Check access level
    access_level = get_resource_access_level(
        user_role=UserRole(current_user["user_role"]),
        resource_type="project",
        user_id=current_user["user_id"],
        resource_owner_id=project["project_manager_id"],
        resource_id=project_id
    )
    
    if access_level == AccessLevel.NO_ACCESS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to view this project"
        )
    
    return ProjectResponse(
        id=project["_id"],
        name=project["name"],
        code=project["code"],
        description=project["description"],
        project_type=project["project_type"],
        methodology=project["methodology"],
        status=project["status"],
        health_status=project["health_status"],
        priority=project["priority"],
        portfolio_id=project["portfolio_id"],
        project_manager_id=project["project_manager_id"],
        sponsor_id=project["sponsor_id"],
        planned_start_date=project["planned_start_date"],
        planned_end_date=project["planned_end_date"],
        actual_start_date=project["actual_start_date"],
        actual_end_date=project["actual_end_date"],
        percent_complete=project["percent_complete"],
        financials=project["financials"],
        risk_score=project["risk_score"],
        open_issues_count=project["open_issues_count"],
        open_risks_count=project["open_risks_count"],
        team_size=len(project["team_members"]),
        created_at=project["created_at"],
        updated_at=project["updated_at"]
    )

@router.put("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """Update project"""
    db = await get_database()
    projects_collection = db.get_default_database().projects
    
    # Get existing project
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
    
    # Check access level
    access_level = get_resource_access_level(
        user_role=UserRole(current_user["user_role"]),
        resource_type="project",
        user_id=current_user["user_id"],
        resource_owner_id=project["project_manager_id"],
        resource_id=project_id
    )
    
    if access_level not in [AccessLevel.FULL, AccessLevel.READ_WRITE]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to update this project"
        )
    
    # Prepare update data
    update_data = project_data.dict(exclude_unset=True)
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        update_data["updated_by"] = current_user["user_id"]
        
        await projects_collection.update_one(
            {"_id": project_id},
            {"$set": update_data}
        )
        
        # Get updated project
        updated_project = await projects_collection.find_one({"_id": project_id})
        
        return ProjectResponse(
            id=updated_project["_id"],
            name=updated_project["name"],
            code=updated_project["code"],
            description=updated_project["description"],
            project_type=updated_project["project_type"],
            methodology=updated_project["methodology"],
            status=updated_project["status"],
            health_status=updated_project["health_status"],
            priority=updated_project["priority"],
            portfolio_id=updated_project["portfolio_id"],
            project_manager_id=updated_project["project_manager_id"],
            sponsor_id=updated_project["sponsor_id"],
            planned_start_date=updated_project["planned_start_date"],
            planned_end_date=updated_project["planned_end_date"],
            actual_start_date=updated_project["actual_start_date"],
            actual_end_date=updated_project["actual_end_date"],
            percent_complete=updated_project["percent_complete"],
            financials=updated_project["financials"],
            risk_score=updated_project["risk_score"],
            open_issues_count=updated_project["open_issues_count"],
            open_risks_count=updated_project["open_risks_count"],
            team_size=len(updated_project["team_members"]),
            created_at=updated_project["created_at"],
            updated_at=updated_project["updated_at"]
        )
    
    # Return unchanged project if no updates
    return ProjectResponse(
        id=project["_id"],
        name=project["name"],
        code=project["code"],
        description=project["description"],
        project_type=project["project_type"],
        methodology=project["methodology"],
        status=project["status"],
        health_status=project["health_status"],
        priority=project["priority"],
        portfolio_id=project["portfolio_id"],
        project_manager_id=project["project_manager_id"],
        sponsor_id=project["sponsor_id"],
        planned_start_date=project["planned_start_date"],
        planned_end_date=project["planned_end_date"],
        actual_start_date=project["actual_start_date"],
        actual_end_date=project["actual_end_date"],
        percent_complete=project["percent_complete"],
        financials=project["financials"],
        risk_score=project["risk_score"],
        open_issues_count=project["open_issues_count"],
        open_risks_count=project["open_risks_count"],
        team_size=len(project["team_members"]),
        created_at=project["created_at"],
        updated_at=project["updated_at"]
    )
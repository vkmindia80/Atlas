from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer
from typing import List, Optional
from ...core.database import get_database
from ...core.middleware import get_current_user_and_tenant
from ...models.task import (
    TaskCreate, TaskUpdate, TaskResponse, Task, TaskType, TaskStatus,
    Priority, BulkTaskUpdate, TaskFilter, TaskDependency, DependencyType
)
from ...models.user import UserRole
from ...utils.rbac import Permission, user_has_permission, get_resource_access_level, AccessLevel
from datetime import datetime, date
import uuid

router = APIRouter()
security = HTTPBearer()

async def get_current_user_with_permissions(credentials = Depends(security)):
    """Get current user with permission checking"""
    return await get_current_user_and_tenant(credentials)

@router.post("/tasks", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """Create a new task"""
    if not user_has_permission(UserRole(current_user["user_role"]), Permission.CREATE_TASK):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to create task"
        )
    
    db = await get_database()
    tasks_collection = db.get_default_database().tasks
    projects_collection = db.get_default_database().projects
    
    # Verify project exists and user has access
    project = await projects_collection.find_one({
        "_id": task_data.project_id,
        "tenant_id": current_user["tenant_id"],
        "is_active": True
    })
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project not found"
        )
    
    # Create task document
    task_id = str(uuid.uuid4())
    task_doc = {
        "_id": task_id,
        "tenant_id": current_user["tenant_id"],
        "name": task_data.name,
        "description": task_data.description,
        "task_type": task_data.task_type,
        "status": "todo",
        "priority": task_data.priority,
        "project_id": task_data.project_id,
        "parent_task_id": task_data.parent_task_id,
        "milestone_id": task_data.milestone_id,
        "assignments": [],
        "planned_start_date": task_data.planned_start_date,
        "planned_end_date": task_data.planned_end_date,
        "actual_start_date": None,
        "actual_end_date": None,
        "estimated_hours": task_data.estimated_hours,
        "remaining_hours": task_data.estimated_hours,
        "percent_complete": 0.0,
        "dependencies": [],
        "time_entries": [],
        "labels": task_data.labels,
        "tags": task_data.tags,
        "story_points": task_data.story_points,
        "business_value": None,
        "board_column": "todo",
        "board_position": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "created_by": current_user["user_id"],
        "is_active": True,
        "metadata": {}
    }
    
    await tasks_collection.insert_one(task_doc)
    
    return TaskResponse(
        id=task_doc["_id"],
        name=task_doc["name"],
        description=task_doc["description"],
        task_type=task_doc["task_type"],
        status=TaskStatus(task_doc["status"]),
        priority=Priority(task_doc["priority"]),
        project_id=task_doc["project_id"],
        parent_task_id=task_doc["parent_task_id"],
        milestone_id=task_doc["milestone_id"],
        planned_start_date=task_doc["planned_start_date"],
        planned_end_date=task_doc["planned_end_date"],
        actual_start_date=task_doc["actual_start_date"],
        actual_end_date=task_doc["actual_end_date"],
        estimated_hours=task_doc["estimated_hours"],
        remaining_hours=task_doc["remaining_hours"],
        percent_complete=task_doc["percent_complete"],
        story_points=task_doc["story_points"],
        business_value=task_doc["business_value"],
        board_column=task_doc["board_column"],
        board_position=task_doc["board_position"],
        labels=task_doc["labels"],
        tags=task_doc["tags"],
        assignments=task_doc["assignments"],
        dependencies=task_doc["dependencies"],
        total_time_logged=0.0,
        created_at=task_doc["created_at"],
        updated_at=task_doc["updated_at"]
    )

@router.get("/tasks", response_model=List[TaskResponse])
async def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    project_id: Optional[str] = None,
    status: Optional[TaskStatus] = None,
    priority: Optional[Priority] = None,
    assignee_id: Optional[str] = None,
    milestone_id: Optional[str] = None,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """List tasks with filtering"""
    if not user_has_permission(UserRole(current_user["user_role"]), Permission.VIEW_TASK):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to view tasks"
        )
    
    db = await get_database()
    tasks_collection = db.get_default_database().tasks
    
    # Build filter query
    filter_query = {"tenant_id": current_user["tenant_id"], "is_active": True}
    
    if project_id:
        filter_query["project_id"] = project_id
    if status:
        filter_query["status"] = status
    if priority:
        filter_query["priority"] = priority
    if assignee_id:
        filter_query["assignments.user_id"] = assignee_id
    if milestone_id:
        filter_query["milestone_id"] = milestone_id
    
    # Execute query with sorting
    cursor = tasks_collection.find(filter_query).sort("created_at", -1).skip(skip).limit(limit)
    tasks = await cursor.to_list(length=limit)
    
    return [
        TaskResponse(
            id=task["_id"],
            name=task["name"],
            description=task["description"],
            task_type=TaskType(task["task_type"]),
            status=TaskStatus(task["status"]),
            priority=Priority(task["priority"]),
            project_id=task["project_id"],
            parent_task_id=task["parent_task_id"],
            milestone_id=task["milestone_id"],
            planned_start_date=task["planned_start_date"],
            planned_end_date=task["planned_end_date"],
            actual_start_date=task["actual_start_date"],
            actual_end_date=task["actual_end_date"],
            estimated_hours=task["estimated_hours"],
            remaining_hours=task["remaining_hours"],
            percent_complete=task["percent_complete"],
            story_points=task["story_points"],
            business_value=task.get("business_value"),
            board_column=task["board_column"],
            board_position=task["board_position"],
            labels=task["labels"],
            tags=task["tags"],
            assignments=task["assignments"],
            dependencies=task["dependencies"],
            total_time_logged=sum(entry.get("hours", 0) for entry in task.get("time_entries", [])),
            created_at=task["created_at"],
            updated_at=task["updated_at"]
        )
        for task in tasks
    ]

@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """Get task by ID"""
    db = await get_database()
    tasks_collection = db.get_default_database().tasks
    
    task = await tasks_collection.find_one({
        "_id": task_id,
        "tenant_id": current_user["tenant_id"],
        "is_active": True
    })
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return TaskResponse(
        id=task["_id"],
        name=task["name"],
        description=task["description"],
        task_type=TaskType(task["task_type"]),
        status=TaskStatus(task["status"]),
        priority=Priority(task["priority"]),
        project_id=task["project_id"],
        parent_task_id=task["parent_task_id"],
        milestone_id=task["milestone_id"],
        planned_start_date=task["planned_start_date"],
        planned_end_date=task["planned_end_date"],
        actual_start_date=task["actual_start_date"],
        actual_end_date=task["actual_end_date"],
        estimated_hours=task["estimated_hours"],
        remaining_hours=task["remaining_hours"],
        percent_complete=task["percent_complete"],
        story_points=task["story_points"],
        business_value=task.get("business_value"),
        board_column=task["board_column"],
        board_position=task["board_position"],
        labels=task["labels"],
        tags=task["tags"],
        assignments=task["assignments"],
        dependencies=task["dependencies"],
        total_time_logged=sum(entry.get("hours", 0) for entry in task.get("time_entries", [])),
        created_at=task["created_at"],
        updated_at=task["updated_at"]
    )

@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """Update task"""
    db = await get_database()
    tasks_collection = db.get_default_database().tasks
    
    # Get existing task
    task = await tasks_collection.find_one({
        "_id": task_id,
        "tenant_id": current_user["tenant_id"],
        "is_active": True
    })
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Prepare update data
    update_data = task_data.dict(exclude_unset=True)
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        update_data["updated_by"] = current_user["user_id"]
        
        await tasks_collection.update_one(
            {"_id": task_id},
            {"$set": update_data}
        )
        
        # Get updated task
        updated_task = await tasks_collection.find_one({"_id": task_id})
        
        return TaskResponse(
            id=updated_task["_id"],
            name=updated_task["name"],
            description=updated_task["description"],
            task_type=TaskType(updated_task["task_type"]),
            status=TaskStatus(updated_task["status"]),
            priority=Priority(updated_task["priority"]),
            project_id=updated_task["project_id"],
            parent_task_id=updated_task["parent_task_id"],
            milestone_id=updated_task["milestone_id"],
            planned_start_date=updated_task["planned_start_date"],
            planned_end_date=updated_task["planned_end_date"],
            actual_start_date=updated_task["actual_start_date"],
            actual_end_date=updated_task["actual_end_date"],
            estimated_hours=updated_task["estimated_hours"],
            remaining_hours=updated_task["remaining_hours"],
            percent_complete=updated_task["percent_complete"],
            story_points=updated_task["story_points"],
            business_value=updated_task.get("business_value"),
            board_column=updated_task["board_column"],
            board_position=updated_task["board_position"],
            labels=updated_task["labels"],
            tags=updated_task["tags"],
            assignments=updated_task["assignments"],
            dependencies=updated_task["dependencies"],
            total_time_logged=sum(entry.get("hours", 0) for entry in updated_task.get("time_entries", [])),
            created_at=updated_task["created_at"],
            updated_at=updated_task["updated_at"]
        )

@router.post("/tasks/{task_id}/dependencies")
async def add_task_dependency(
    task_id: str,
    dependency_data: dict,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """Add dependency to task"""
    db = await get_database()
    tasks_collection = db.get_default_database().tasks
    
    # Verify both tasks exist
    task = await tasks_collection.find_one({"_id": task_id, "tenant_id": current_user["tenant_id"]})
    predecessor_task = await tasks_collection.find_one({
        "_id": dependency_data["predecessor_task_id"], 
        "tenant_id": current_user["tenant_id"]
    })
    
    if not task or not predecessor_task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task not found"
        )
    
    # Create dependency
    dependency = TaskDependency(
        predecessor_task_id=dependency_data["predecessor_task_id"],
        successor_task_id=task_id,
        dependency_type=DependencyType(dependency_data.get("dependency_type", "finish_to_start")),
        lag_days=dependency_data.get("lag_days", 0)
    )
    
    # Add to task
    await tasks_collection.update_one(
        {"_id": task_id},
        {"$push": {"dependencies": dependency.dict()}}
    )
    
    return {"message": "Dependency added successfully"}

@router.post("/tasks/bulk", response_model=dict)
async def bulk_update_tasks(
    bulk_data: BulkTaskUpdate,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """Bulk update tasks"""
    if not user_has_permission(UserRole(current_user["user_role"]), Permission.UPDATE_TASK):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to update tasks"
        )
    
    db = await get_database()
    tasks_collection = db.get_default_database().tasks
    
    # Prepare update data
    update_data = bulk_data.updates.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    update_data["updated_by"] = current_user["user_id"]
    
    # Update tasks
    result = await tasks_collection.update_many(
        {
            "_id": {"$in": bulk_data.task_ids},
            "tenant_id": current_user["tenant_id"],
            "is_active": True
        },
        {"$set": update_data}
    )
    
    return {
        "updated_count": result.modified_count,
        "task_ids": bulk_data.task_ids
    }
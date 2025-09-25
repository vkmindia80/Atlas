from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer
from typing import List, Dict, Any
from ...core.database import get_database
from ...core.middleware import get_current_user_and_tenant
from ...models.tenant import TenantResponse, TenantUpdate, TenantStatus
from ...models.user import UserRole
from ...utils.rbac import Permission, user_has_permission
from datetime import datetime

router = APIRouter()
security = HTTPBearer()

async def get_current_user_with_permissions(credentials = Depends(security)):
    """Get current user with permission checking"""
    return await get_current_user_and_tenant(credentials)

@router.get("/admin/dashboard", response_model=Dict[str, Any])
async def get_admin_dashboard(
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """Get admin dashboard statistics"""
    # Only admins and PMO admins can access
    if current_user["user_role"] not in [UserRole.ADMIN, UserRole.PMO_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to access admin dashboard"
        )
    
    db = await get_database()
    
    # Get collections
    users_collection = db.get_default_database().users
    portfolios_collection = db.get_default_database().portfolios
    projects_collection = db.get_default_database().projects
    
    # Basic statistics
    users_count = await users_collection.count_documents({
        "tenant_id": current_user["tenant_id"],
        "is_active": True
    })
    
    portfolios_count = await portfolios_collection.count_documents({
        "tenant_id": current_user["tenant_id"],
        "is_active": True
    })
    
    projects_count = await projects_collection.count_documents({
        "tenant_id": current_user["tenant_id"],
        "is_active": True
    })
    
    # Active projects by status
    active_projects_pipeline = [
        {"$match": {"tenant_id": current_user["tenant_id"], "is_active": True}},
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ]
    project_status_counts = {}
    async for result in projects_collection.aggregate(active_projects_pipeline):
        project_status_counts[result["_id"]] = result["count"]
    
    # Users by role
    users_by_role_pipeline = [
        {"$match": {"tenant_id": current_user["tenant_id"], "is_active": True}},
        {"$group": {"_id": "$role", "count": {"$sum": 1}}}
    ]
    users_by_role = {}
    async for result in users_collection.aggregate(users_by_role_pipeline):
        users_by_role[result["_id"]] = result["count"]
    
    # Recent activity (last 30 days)
    from datetime import timedelta
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    recent_users = await users_collection.count_documents({
        "tenant_id": current_user["tenant_id"],
        "created_at": {"$gte": thirty_days_ago}
    })
    
    recent_projects = await projects_collection.count_documents({
        "tenant_id": current_user["tenant_id"],
        "created_at": {"$gte": thirty_days_ago}
    })
    
    return {
        "overview": {
            "total_users": users_count,
            "total_portfolios": portfolios_count,
            "total_projects": projects_count
        },
        "project_status_distribution": project_status_counts,
        "users_by_role": users_by_role,
        "recent_activity": {
            "new_users_30_days": recent_users,
            "new_projects_30_days": recent_projects
        }
    }

@router.get("/admin/tenant", response_model=TenantResponse)
async def get_tenant_info(
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """Get current tenant information"""
    # Check permissions
    if not user_has_permission(UserRole(current_user["user_role"]), Permission.VIEW_TENANT):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to view tenant information"
        )
    
    db = await get_database()
    tenants_collection = db.get_default_database().tenants
    
    tenant = await tenants_collection.find_one({"_id": current_user["tenant_id"]})
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )
    
    return TenantResponse(
        id=tenant["_id"],
        name=tenant["name"],
        code=tenant["code"],
        domain=tenant["domain"],
        status=tenant["status"],
        plan=tenant["plan"],
        admin_email=tenant["admin_email"],
        admin_name=tenant["admin_name"],
        max_users=tenant["max_users"],
        max_projects=tenant["max_projects"],
        created_at=tenant["created_at"],
        updated_at=tenant["updated_at"]
    )

@router.put("/admin/tenant", response_model=TenantResponse)
async def update_tenant(
    tenant_data: TenantUpdate,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """Update tenant information"""
    # Check permissions
    if not user_has_permission(UserRole(current_user["user_role"]), Permission.MANAGE_TENANT):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to update tenant"
        )
    
    db = await get_database()
    tenants_collection = db.get_default_database().tenants
    
    # Prepare update data
    update_data = tenant_data.dict(exclude_unset=True)
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        
        result = await tenants_collection.update_one(
            {"_id": current_user["tenant_id"]},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant not found"
            )
    
    # Get updated tenant
    tenant = await tenants_collection.find_one({"_id": current_user["tenant_id"]})
    
    return TenantResponse(
        id=tenant["_id"],
        name=tenant["name"],
        code=tenant["code"],
        domain=tenant["domain"],
        status=tenant["status"],
        plan=tenant["plan"],
        admin_email=tenant["admin_email"],
        admin_name=tenant["admin_name"],
        max_users=tenant["max_users"],
        max_projects=tenant["max_projects"],
        created_at=tenant["created_at"],
        updated_at=tenant["updated_at"]
    )

@router.get("/admin/audit-logs")
async def get_audit_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    resource_type: str = None,
    action: str = None,
    user_id: str = None,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """Get audit logs (placeholder for future implementation)"""
    # Check permissions
    if not user_has_permission(UserRole(current_user["user_role"]), Permission.VIEW_AUDIT_LOGS):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to view audit logs"
        )
    
    # This is a placeholder - actual audit logging would be implemented
    # with a separate audit collection and proper event tracking
    return {
        "message": "Audit logging system will be implemented in Phase 4",
        "total": 0,
        "logs": []
    }

@router.get("/admin/system-health")
async def get_system_health(
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """Get system health status"""
    # Check permissions
    if current_user["user_role"] != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only platform admins can access system health"
        )
    
    db = await get_database()
    
    # Basic health checks
    try:
        # Check database connectivity
        await db.admin.command("ping")
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "database": db_status,
            "api": "healthy"
        }
    }
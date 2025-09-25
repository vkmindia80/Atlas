from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer
from typing import List, Optional
from ...core.database import get_database
from ...core.security import get_password_hash
from ...core.middleware import get_current_user_and_tenant
from ...models.user import UserCreate, UserUpdate, UserResponse, UserRole, UserStatus
from ...utils.rbac import Permission, user_has_permission
from datetime import datetime
import uuid

router = APIRouter()
security = HTTPBearer()

async def get_current_user_with_permissions(credentials = Depends(security)):
    """Get current user with permission checking"""
    return await get_current_user_and_tenant(credentials)

@router.post("/users", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """Create a new user (requires MANAGE_USERS permission)"""
    # Check permissions
    if not user_has_permission(UserRole(current_user["user_role"]), Permission.MANAGE_USERS):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to create users"
        )
    
    db = await get_database()
    users_collection = db.get_default_database().users
    
    # Check if username or email already exists in tenant
    existing_user = await users_collection.find_one({
        "$or": [
            {"username": user_data.username, "tenant_id": current_user["tenant_id"]},
            {"email": user_data.email, "tenant_id": current_user["tenant_id"]}
        ]
    })
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )
    
    # Create user document
    user_id = str(uuid.uuid4())
    user_doc = {
        "_id": user_id,
        "tenant_id": current_user["tenant_id"],
        "username": user_data.username,
        "email": user_data.email,
        "full_name": user_data.full_name,
        "hashed_password": get_password_hash(user_data.password),
        "role": user_data.role,
        "status": UserStatus.PENDING_VERIFICATION,
        "job_title": user_data.job_title,
        "department": user_data.department,
        "phone": user_data.phone,
        "permissions": [],
        "portfolio_access": [],
        "project_access": [],
        "preferences": {},
        "failed_login_attempts": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "created_by": current_user["user_id"],
        "is_active": True,
        "metadata": {}
    }
    
    await users_collection.insert_one(user_doc)
    
    return UserResponse(
        id=user_doc["_id"],
        username=user_doc["username"],
        email=user_doc["email"],
        full_name=user_doc["full_name"],
        role=user_doc["role"],
        status=user_doc["status"],
        job_title=user_doc["job_title"],
        department=user_doc["department"],
        phone=user_doc["phone"],
        avatar_url=user_doc.get("avatar_url"),
        last_login=user_doc.get("last_login"),
        created_at=user_doc["created_at"],
        updated_at=user_doc["updated_at"]
    )

@router.get("/users", response_model=List[UserResponse])
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    role: Optional[UserRole] = None,
    status: Optional[UserStatus] = None,
    department: Optional[str] = None,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """List users with optional filtering"""
    # Check permissions
    if not user_has_permission(UserRole(current_user["user_role"]), Permission.VIEW_USERS):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to view users"
        )
    
    db = await get_database()
    users_collection = db.get_default_database().users
    
    # Build filter query
    filter_query = {"tenant_id": current_user["tenant_id"], "is_active": True}
    
    if role:
        filter_query["role"] = role
    if status:
        filter_query["status"] = status
    if department:
        filter_query["department"] = department
    
    # Execute query
    cursor = users_collection.find(filter_query).skip(skip).limit(limit)
    users = await cursor.to_list(length=limit)
    
    return [
        UserResponse(
            id=user["_id"],
            username=user["username"],
            email=user["email"],
            full_name=user["full_name"],
            role=user["role"],
            status=user["status"],
            job_title=user.get("job_title"),
            department=user.get("department"),
            phone=user.get("phone"),
            avatar_url=user.get("avatar_url"),
            last_login=user.get("last_login"),
            created_at=user["created_at"],
            updated_at=user["updated_at"]
        )
        for user in users
    ]

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """Get user by ID"""
    # Check permissions
    if not user_has_permission(UserRole(current_user["user_role"]), Permission.VIEW_USERS):
        # Allow users to view their own profile
        if user_id != current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to view user"
            )
    
    db = await get_database()
    users_collection = db.get_default_database().users
    
    user = await users_collection.find_one({
        "_id": user_id,
        "tenant_id": current_user["tenant_id"],
        "is_active": True
    })
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        id=user["_id"],
        username=user["username"],
        email=user["email"],
        full_name=user["full_name"],
        role=user["role"],
        status=user["status"],
        job_title=user.get("job_title"),
        department=user.get("department"),
        phone=user.get("phone"),
        avatar_url=user.get("avatar_url"),
        last_login=user.get("last_login"),
        created_at=user["created_at"],
        updated_at=user["updated_at"]
    )

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """Update user"""
    # Check permissions
    if not user_has_permission(UserRole(current_user["user_role"]), Permission.MANAGE_USERS):
        # Allow users to update their own profile (limited fields)
        if user_id != current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to update user"
            )
        
        # Restrict fields for self-update
        allowed_fields = {"full_name", "phone", "avatar_url"}
        update_fields = {k for k, v in user_data.dict(exclude_unset=True).items() if v is not None}
        if not update_fields.issubset(allowed_fields):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot update restricted fields"
            )
    
    db = await get_database()
    users_collection = db.get_default_database().users
    
    # Get existing user
    user = await users_collection.find_one({
        "_id": user_id,
        "tenant_id": current_user["tenant_id"],
        "is_active": True
    })
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prepare update data
    update_data = user_data.dict(exclude_unset=True)
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        update_data["updated_by"] = current_user["user_id"]
        
        await users_collection.update_one(
            {"_id": user_id},
            {"$set": update_data}
        )
        
        # Get updated user
        updated_user = await users_collection.find_one({"_id": user_id})
        
        return UserResponse(
            id=updated_user["_id"],
            username=updated_user["username"],
            email=updated_user["email"],
            full_name=updated_user["full_name"],
            role=updated_user["role"],
            status=updated_user["status"],
            job_title=updated_user.get("job_title"),
            department=updated_user.get("department"),
            phone=updated_user.get("phone"),
            avatar_url=updated_user.get("avatar_url"),
            last_login=updated_user.get("last_login"),
            created_at=updated_user["created_at"],
            updated_at=updated_user["updated_at"]
        )
    
    return UserResponse(
        id=user["_id"],
        username=user["username"],
        email=user["email"],
        full_name=user["full_name"],
        role=user["role"],
        status=user["status"],
        job_title=user.get("job_title"),
        department=user.get("department"),
        phone=user.get("phone"),
        avatar_url=user.get("avatar_url"),
        last_login=user.get("last_login"),
        created_at=user["created_at"],
        updated_at=user["updated_at"]
    )

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """Soft delete user (deactivate)"""
    # Check permissions
    if not user_has_permission(UserRole(current_user["user_role"]), Permission.MANAGE_USERS):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to delete user"
        )
    
    # Prevent self-deletion
    if user_id == current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    db = await get_database()
    users_collection = db.get_default_database().users
    
    result = await users_collection.update_one(
        {"_id": user_id, "tenant_id": current_user["tenant_id"]},
        {
            "$set": {
                "is_active": False,
                "status": UserStatus.INACTIVE,
                "updated_at": datetime.utcnow(),
                "updated_by": current_user["user_id"]
            }
        }
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User deactivated successfully"}
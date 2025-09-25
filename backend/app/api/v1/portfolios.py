from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer
from typing import List, Optional
from ...core.database import get_database
from ...core.middleware import get_current_user_and_tenant
from ...models.portfolio import (
    PortfolioCreate, PortfolioUpdate, PortfolioResponse, 
    Portfolio, PortfolioType, Priority, Status
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

@router.post("/portfolios", response_model=PortfolioResponse)
async def create_portfolio(
    portfolio_data: PortfolioCreate,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """Create a new portfolio"""
    # Check permissions
    if not user_has_permission(UserRole(current_user["user_role"]), Permission.CREATE_PORTFOLIO):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to create portfolio"
        )
    
    db = await get_database()
    portfolios_collection = db.get_default_database().portfolios
    
    # Check if portfolio code already exists in tenant
    existing_portfolio = await portfolios_collection.find_one({
        "code": portfolio_data.code,
        "tenant_id": current_user["tenant_id"]
    })
    
    if existing_portfolio:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Portfolio code already exists"
        )
    
    # Create portfolio document
    portfolio_id = str(uuid.uuid4())
    portfolio_doc = {
        "_id": portfolio_id,
        "tenant_id": current_user["tenant_id"],
        "name": portfolio_data.name,
        "code": portfolio_data.code,
        "description": portfolio_data.description,
        "portfolio_type": portfolio_data.portfolio_type,
        "status": Status.DRAFT,
        "health_status": "green",
        "priority": portfolio_data.priority,
        "portfolio_manager_id": portfolio_data.portfolio_manager_id,
        "sponsors": portfolio_data.sponsors,
        "stakeholders": portfolio_data.stakeholders,
        "strategic_objectives": [],
        "business_case_url": portfolio_data.business_case_url,
        "start_date": portfolio_data.start_date,
        "end_date": portfolio_data.end_date,
        "financial_metrics": {
            "total_budget": 0,
            "allocated_budget": 0,
            "spent_amount": 0,
            "committed_amount": 0,
            "forecasted_cost": 0
        },
        "risk_metrics": {
            "risk_score": 0.0,
            "high_risks_count": 0,
            "medium_risks_count": 0,
            "low_risks_count": 0,
            "overdue_risks_count": 0
        },
        "project_ids": [],
        "settings": {},
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "created_by": current_user["user_id"],
        "is_active": True,
        "metadata": {}
    }
    
    await portfolios_collection.insert_one(portfolio_doc)
    
    return PortfolioResponse(
        id=portfolio_doc["_id"],
        name=portfolio_doc["name"],
        code=portfolio_doc["code"],
        description=portfolio_doc["description"],
        portfolio_type=portfolio_doc["portfolio_type"],
        status=portfolio_doc["status"],
        health_status=portfolio_doc["health_status"],
        priority=portfolio_doc["priority"],
        portfolio_manager_id=portfolio_doc["portfolio_manager_id"],
        sponsors=portfolio_doc["sponsors"],
        stakeholders=portfolio_doc["stakeholders"],
        start_date=portfolio_doc["start_date"],
        end_date=portfolio_doc["end_date"],
        financial_metrics=portfolio_doc["financial_metrics"],
        risk_metrics=portfolio_doc["risk_metrics"],
        project_count=len(portfolio_doc["project_ids"]),
        created_at=portfolio_doc["created_at"],
        updated_at=portfolio_doc["updated_at"]
    )

@router.get("/portfolios", response_model=List[PortfolioResponse])
async def list_portfolios(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    portfolio_type: Optional[PortfolioType] = None,
    status: Optional[Status] = None,
    priority: Optional[Priority] = None,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """List portfolios with optional filtering"""
    # Check permissions
    if not user_has_permission(UserRole(current_user["user_role"]), Permission.VIEW_PORTFOLIO):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to view portfolios"
        )
    
    db = await get_database()
    portfolios_collection = db.get_default_database().portfolios
    
    # Build filter query
    filter_query = {"tenant_id": current_user["tenant_id"], "is_active": True}
    
    if portfolio_type:
        filter_query["portfolio_type"] = portfolio_type
    if status:
        filter_query["status"] = status
    if priority:
        filter_query["priority"] = priority
    
    # Execute query
    cursor = portfolios_collection.find(filter_query).skip(skip).limit(limit)
    portfolios = await cursor.to_list(length=limit)
    
    return [
        PortfolioResponse(
            id=portfolio["_id"],
            name=portfolio["name"],
            code=portfolio["code"],
            description=portfolio["description"],
            portfolio_type=portfolio["portfolio_type"],
            status=portfolio["status"],
            health_status=portfolio["health_status"],
            priority=portfolio["priority"],
            portfolio_manager_id=portfolio["portfolio_manager_id"],
            sponsors=portfolio["sponsors"],
            stakeholders=portfolio["stakeholders"],
            start_date=portfolio["start_date"],
            end_date=portfolio["end_date"],
            financial_metrics=portfolio["financial_metrics"],
            risk_metrics=portfolio["risk_metrics"],
            project_count=len(portfolio["project_ids"]),
            created_at=portfolio["created_at"],
            updated_at=portfolio["updated_at"]
        )
        for portfolio in portfolios
    ]

@router.get("/portfolios/{portfolio_id}", response_model=PortfolioResponse)
async def get_portfolio(
    portfolio_id: str,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """Get portfolio by ID"""
    db = await get_database()
    portfolios_collection = db.get_default_database().portfolios
    
    portfolio = await portfolios_collection.find_one({
        "_id": portfolio_id,
        "tenant_id": current_user["tenant_id"],
        "is_active": True
    })
    
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )
    
    # Check access level
    access_level = get_resource_access_level(
        user_role=UserRole(current_user["user_role"]),
        resource_type="portfolio",
        user_id=current_user["user_id"],
        resource_owner_id=portfolio["portfolio_manager_id"],
        resource_id=portfolio_id
    )
    
    if access_level == AccessLevel.NO_ACCESS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to view this portfolio"
        )
    
    return PortfolioResponse(
        id=portfolio["_id"],
        name=portfolio["name"],
        code=portfolio["code"],
        description=portfolio["description"],
        portfolio_type=portfolio["portfolio_type"],
        status=portfolio["status"],
        health_status=portfolio["health_status"],
        priority=portfolio["priority"],
        portfolio_manager_id=portfolio["portfolio_manager_id"],
        sponsors=portfolio["sponsors"],
        stakeholders=portfolio["stakeholders"],
        start_date=portfolio["start_date"],
        end_date=portfolio["end_date"],
        financial_metrics=portfolio["financial_metrics"],
        risk_metrics=portfolio["risk_metrics"],
        project_count=len(portfolio["project_ids"]),
        created_at=portfolio["created_at"],
        updated_at=portfolio["updated_at"]
    )

@router.put("/portfolios/{portfolio_id}", response_model=PortfolioResponse)
async def update_portfolio(
    portfolio_id: str,
    portfolio_data: PortfolioUpdate,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """Update portfolio"""
    db = await get_database()
    portfolios_collection = db.get_default_database().portfolios
    
    # Get existing portfolio
    portfolio = await portfolios_collection.find_one({
        "_id": portfolio_id,
        "tenant_id": current_user["tenant_id"],
        "is_active": True
    })
    
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )
    
    # Check access level
    access_level = get_resource_access_level(
        user_role=UserRole(current_user["user_role"]),
        resource_type="portfolio",
        user_id=current_user["user_id"],
        resource_owner_id=portfolio["portfolio_manager_id"],
        resource_id=portfolio_id
    )
    
    if access_level not in [AccessLevel.FULL, AccessLevel.READ_WRITE]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to update this portfolio"
        )
    
    # Prepare update data
    update_data = portfolio_data.dict(exclude_unset=True)
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        update_data["updated_by"] = current_user["user_id"]
        
        await portfolios_collection.update_one(
            {"_id": portfolio_id},
            {"$set": update_data}
        )
        
        # Get updated portfolio
        updated_portfolio = await portfolios_collection.find_one({"_id": portfolio_id})
        
        return PortfolioResponse(
            id=updated_portfolio["_id"],
            name=updated_portfolio["name"],
            code=updated_portfolio["code"],
            description=updated_portfolio["description"],
            portfolio_type=updated_portfolio["portfolio_type"],
            status=updated_portfolio["status"],
            health_status=updated_portfolio["health_status"],
            priority=updated_portfolio["priority"],
            portfolio_manager_id=updated_portfolio["portfolio_manager_id"],
            sponsors=updated_portfolio["sponsors"],
            stakeholders=updated_portfolio["stakeholders"],
            start_date=updated_portfolio["start_date"],
            end_date=updated_portfolio["end_date"],
            financial_metrics=updated_portfolio["financial_metrics"],
            risk_metrics=updated_portfolio["risk_metrics"],
            project_count=len(updated_portfolio["project_ids"]),
            created_at=updated_portfolio["created_at"],
            updated_at=updated_portfolio["updated_at"]
        )
    
    # Return unchanged portfolio if no updates
    return PortfolioResponse(
        id=portfolio["_id"],
        name=portfolio["name"],
        code=portfolio["code"],
        description=portfolio["description"],
        portfolio_type=portfolio["portfolio_type"],
        status=portfolio["status"],
        health_status=portfolio["health_status"],
        priority=portfolio["priority"],
        portfolio_manager_id=portfolio["portfolio_manager_id"],
        sponsors=portfolio["sponsors"],
        stakeholders=portfolio["stakeholders"],
        start_date=portfolio["start_date"],
        end_date=portfolio["end_date"],
        financial_metrics=portfolio["financial_metrics"],
        risk_metrics=portfolio["risk_metrics"],
        project_count=len(portfolio["project_ids"]),
        created_at=portfolio["created_at"],
        updated_at=portfolio["updated_at"]
    )
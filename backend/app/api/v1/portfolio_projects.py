from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer
from typing import List, Optional
from ...core.database import get_database
from ...core.middleware import get_current_user_and_tenant
from ...models.portfolio_project import (
    PortfolioProjectCreate, PortfolioProjectUpdate, PortfolioProjectResponse,
    PortfolioProject, PortfolioProjectRelationshipType, PortfolioProjectStatus,
    PortfolioAnalytics, BulkPortfolioProjectOperation
)
from ...models.user import UserRole
from ...utils.rbac import Permission, user_has_permission
from datetime import datetime
from decimal import Decimal
import uuid

router = APIRouter()
security = HTTPBearer()

async def get_current_user_with_permissions(credentials = Depends(security)):
    """Get current user with permission checking"""
    return await get_current_user_and_tenant(credentials)

@router.post("/portfolio-projects", response_model=PortfolioProjectResponse)
async def create_portfolio_project_relationship(
    relationship_data: PortfolioProjectCreate,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """Create portfolio-project relationship"""
    if not user_has_permission(UserRole(current_user["user_role"]), Permission.CREATE_PORTFOLIO):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to manage portfolio relationships"
        )
    
    db = await get_database()
    portfolio_projects_collection = db.get_default_database().portfolio_projects
    portfolios_collection = db.get_default_database().portfolios
    projects_collection = db.get_default_database().projects
    
    # Verify portfolio and project exist
    portfolio = await portfolios_collection.find_one({
        "_id": relationship_data.portfolio_id,
        "tenant_id": current_user["tenant_id"]
    })
    
    project = await projects_collection.find_one({
        "_id": relationship_data.project_id,
        "tenant_id": current_user["tenant_id"]
    })
    
    if not portfolio or not project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Portfolio or project not found"
        )
    
    # Check if relationship already exists
    existing = await portfolio_projects_collection.find_one({
        "portfolio_id": relationship_data.portfolio_id,
        "project_id": relationship_data.project_id,
        "tenant_id": current_user["tenant_id"]
    })
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Portfolio-project relationship already exists"
        )
    
    # Create relationship
    relationship_id = str(uuid.uuid4())
    relationship_doc = {
        "_id": relationship_id,
        "tenant_id": current_user["tenant_id"],
        "portfolio_id": relationship_data.portfolio_id,
        "project_id": relationship_data.project_id,
        "relationship_type": relationship_data.relationship_type,
        "status": "active",
        "allocated_budget": relationship_data.allocated_budget or 0,
        "budget_percentage": relationship_data.budget_percentage,
        "strategic_objective_ids": relationship_data.strategic_objective_ids,
        "alignment_score": relationship_data.alignment_score or 0.0,
        "contribution_weight": relationship_data.contribution_weight or 1.0,
        "portfolio_phase": relationship_data.portfolio_phase,
        "expected_value_delivery_date": relationship_data.expected_value_delivery_date,
        "resource_rules": {
            "max_budget_percentage": None,
            "max_team_size": None,
            "priority_multiplier": 1.0
        },
        "review_frequency_days": 30,
        "last_review_date": None,
        "next_review_date": None,
        "value_delivered": 0,
        "roi_calculation": None,
        "risk_adjusted_value": None,
        "dependent_project_ids": [],
        "dependency_project_ids": [],
        "relationship_notes": relationship_data.relationship_notes,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "created_by": current_user["user_id"],
        "is_active": True,
        "metadata": {}
    }
    
    await portfolio_projects_collection.insert_one(relationship_doc)
    
    # Update portfolio project list
    await portfolios_collection.update_one(
        {"_id": relationship_data.portfolio_id},
        {"$addToSet": {"project_ids": relationship_data.project_id}}
    )
    
    return PortfolioProjectResponse(
        id=relationship_doc["_id"],
        portfolio_id=relationship_doc["portfolio_id"],
        project_id=relationship_doc["project_id"],
        relationship_type=relationship_doc["relationship_type"],
        status=PortfolioProjectStatus(relationship_doc["status"]),
        allocated_budget=Decimal(str(relationship_doc["allocated_budget"])),
        budget_percentage=relationship_doc["budget_percentage"],
        strategic_objective_ids=relationship_doc["strategic_objective_ids"],
        alignment_score=relationship_doc["alignment_score"],
        contribution_weight=relationship_doc["contribution_weight"],
        portfolio_phase=relationship_doc["portfolio_phase"],
        expected_value_delivery_date=relationship_doc["expected_value_delivery_date"],
        value_delivered=Decimal(str(relationship_doc["value_delivered"])),
        roi_calculation=relationship_doc["roi_calculation"],
        dependent_project_ids=relationship_doc["dependent_project_ids"],
        dependency_project_ids=relationship_doc["dependency_project_ids"],
        last_review_date=relationship_doc["last_review_date"],
        next_review_date=relationship_doc["next_review_date"],
        created_at=relationship_doc["created_at"],
        updated_at=relationship_doc["updated_at"]
    )

@router.get("/portfolio-projects", response_model=List[PortfolioProjectResponse])
async def list_portfolio_project_relationships(
    portfolio_id: Optional[str] = Query(None),
    project_id: Optional[str] = Query(None),
    relationship_type: Optional[PortfolioProjectRelationshipType] = Query(None),
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """List portfolio-project relationships"""
    db = await get_database()
    portfolio_projects_collection = db.get_default_database().portfolio_projects
    
    filter_query = {"tenant_id": current_user["tenant_id"], "is_active": True}
    
    if portfolio_id:
        filter_query["portfolio_id"] = portfolio_id
    if project_id:
        filter_query["project_id"] = project_id
    if relationship_type:
        filter_query["relationship_type"] = relationship_type
    
    relationships = await portfolio_projects_collection.find(filter_query).to_list(length=None)
    
    return [
        PortfolioProjectResponse(
            id=rel["_id"],
            portfolio_id=rel["portfolio_id"],
            project_id=rel["project_id"],
            relationship_type=PortfolioProjectRelationshipType(rel["relationship_type"]),
            status=PortfolioProjectStatus(rel["status"]),
            allocated_budget=Decimal(str(rel["allocated_budget"])),
            budget_percentage=rel["budget_percentage"],
            strategic_objective_ids=rel["strategic_objective_ids"],
            alignment_score=rel["alignment_score"],
            contribution_weight=rel["contribution_weight"],
            portfolio_phase=rel["portfolio_phase"],
            expected_value_delivery_date=rel["expected_value_delivery_date"],
            value_delivered=Decimal(str(rel["value_delivered"])),
            roi_calculation=rel["roi_calculation"],
            dependent_project_ids=rel["dependent_project_ids"],
            dependency_project_ids=rel["dependency_project_ids"],
            last_review_date=rel["last_review_date"],
            next_review_date=rel["next_review_date"],
            created_at=rel["created_at"],
            updated_at=rel["updated_at"]
        )
        for rel in relationships
    ]

@router.get("/portfolios/{portfolio_id}/analytics", response_model=PortfolioAnalytics)
async def get_portfolio_analytics(
    portfolio_id: str,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """Get portfolio analytics and KPIs"""
    db = await get_database()
    portfolio_projects_collection = db.get_default_database().portfolio_projects
    projects_collection = db.get_default_database().projects
    
    # Get portfolio projects
    portfolio_project_rels = await portfolio_projects_collection.find({
        "portfolio_id": portfolio_id,
        "tenant_id": current_user["tenant_id"],
        "is_active": True
    }).to_list(length=None)
    
    project_ids = [rel["project_id"] for rel in portfolio_project_rels]
    
    if not project_ids:
        return PortfolioAnalytics(
            portfolio_id=portfolio_id,
            total_projects=0,
            active_projects=0,
            completed_projects=0,
            on_hold_projects=0,
            cancelled_projects=0,
            total_budget=Decimal('0'),
            total_allocated=Decimal('0'),
            total_spent=Decimal('0'),
            budget_utilization=0.0,
            average_project_budget=Decimal('0'),
            projects_on_schedule=0,
            projects_delayed=0,
            average_project_duration=0.0,
            total_value_delivered=Decimal('0'),
            average_roi=0.0,
            strategic_alignment_avg=0.0,
            high_risk_projects=0,
            medium_risk_projects=0,
            low_risk_projects=0,
            overall_portfolio_risk=0.0,
            total_team_members=0,
            average_team_utilization=0.0
        )
    
    # Get project details
    projects = await projects_collection.find({
        "_id": {"$in": project_ids},
        "tenant_id": current_user["tenant_id"],
        "is_active": True
    }).to_list(length=None)
    
    # Calculate metrics
    total_projects = len(projects)
    active_projects = len([p for p in projects if p["status"] == "active"])
    completed_projects = len([p for p in projects if p["status"] == "completed"])
    on_hold_projects = len([p for p in projects if p["status"] == "on_hold"])
    cancelled_projects = len([p for p in projects if p["status"] == "cancelled"])
    
    total_budget = sum(Decimal(str(p["financials"]["total_budget"])) for p in projects)
    total_spent = sum(Decimal(str(p["financials"]["spent_amount"])) for p in projects)
    
    budget_utilization = float(total_spent / total_budget) if total_budget > 0 else 0.0
    average_project_budget = total_budget / total_projects if total_projects > 0 else Decimal('0')
    
    # Risk analysis
    high_risk = len([p for p in projects if p.get("risk_score", 0) > 0.7])
    medium_risk = len([p for p in projects if 0.3 < p.get("risk_score", 0) <= 0.7])
    low_risk = len([p for p in projects if p.get("risk_score", 0) <= 0.3])
    
    overall_risk = sum(p.get("risk_score", 0) for p in projects) / total_projects if total_projects > 0 else 0.0
    
    # Strategic alignment
    alignment_scores = [rel["alignment_score"] for rel in portfolio_project_rels]
    strategic_alignment_avg = sum(alignment_scores) / len(alignment_scores) if alignment_scores else 0.0
    
    # Value delivered
    total_value_delivered = sum(Decimal(str(rel["value_delivered"])) for rel in portfolio_project_rels)
    
    return PortfolioAnalytics(
        portfolio_id=portfolio_id,
        total_projects=total_projects,
        active_projects=active_projects,
        completed_projects=completed_projects,
        on_hold_projects=on_hold_projects,
        cancelled_projects=cancelled_projects,
        total_budget=total_budget,
        total_allocated=sum(Decimal(str(rel["allocated_budget"])) for rel in portfolio_project_rels),
        total_spent=total_spent,
        budget_utilization=budget_utilization,
        average_project_budget=average_project_budget,
        projects_on_schedule=0,  # Would need timeline analysis
        projects_delayed=0,      # Would need timeline analysis
        average_project_duration=0.0,  # Would need duration calculation
        total_value_delivered=total_value_delivered,
        average_roi=0.0,  # Would need ROI calculation
        strategic_alignment_avg=strategic_alignment_avg,
        high_risk_projects=high_risk,
        medium_risk_projects=medium_risk,
        low_risk_projects=low_risk,
        overall_portfolio_risk=overall_risk,
        total_team_members=sum(len(p.get("team_members", [])) for p in projects),
        average_team_utilization=0.0  # Would need utilization calculation
    )

@router.post("/portfolio-projects/bulk")
async def bulk_portfolio_project_operations(
    bulk_data: BulkPortfolioProjectOperation,
    current_user: dict = Depends(get_current_user_with_permissions)
):
    """Bulk operations on portfolio-project relationships"""
    if not user_has_permission(UserRole(current_user["user_role"]), Permission.UPDATE_PORTFOLIO):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions for bulk operations"
        )
    
    db = await get_database()
    portfolio_projects_collection = db.get_default_database().portfolio_projects
    
    if bulk_data.operation == "add":
        # Bulk add projects to portfolio
        results = []
        for project_id in bulk_data.project_ids:
            try:
                # Check if relationship already exists
                existing = await portfolio_projects_collection.find_one({
                    "portfolio_id": bulk_data.portfolio_id,
                    "project_id": project_id,
                    "tenant_id": current_user["tenant_id"]
                })
                
                if existing:
                    continue
                
                # Create relationship
                relationship_id = str(uuid.uuid4())
                relationship_doc = {
                    "_id": relationship_id,
                    "tenant_id": current_user["tenant_id"],
                    "portfolio_id": bulk_data.portfolio_id,
                    "project_id": project_id,
                    "relationship_type": "primary",
                    "status": "active",
                    "allocated_budget": 0,
                    "budget_percentage": None,
                    "strategic_objective_ids": [],
                    "alignment_score": 0.0,
                    "contribution_weight": 1.0,
                    "portfolio_phase": None,
                    "expected_value_delivery_date": None,
                    "resource_rules": {
                        "max_budget_percentage": None,
                        "max_team_size": None,
                        "priority_multiplier": 1.0
                    },
                    "review_frequency_days": 30,
                    "last_review_date": None,
                    "next_review_date": None,
                    "value_delivered": 0,
                    "roi_calculation": None,
                    "risk_adjusted_value": None,
                    "dependent_project_ids": [],
                    "dependency_project_ids": [],
                    "relationship_notes": None,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow(),
                    "created_by": current_user["user_id"],
                    "is_active": True,
                    "metadata": {}
                }
                
                await portfolio_projects_collection.insert_one(relationship_doc)
                results.append(relationship_id)
                
            except Exception as e:
                continue
        
        return {"message": f"Added {len(results)} project relationships", "created_ids": results}
    
    elif bulk_data.operation == "remove":
        # Bulk remove projects from portfolio
        result = await portfolio_projects_collection.update_many(
            {
                "portfolio_id": bulk_data.portfolio_id,
                "project_id": {"$in": bulk_data.project_ids},
                "tenant_id": current_user["tenant_id"]
            },
            {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
        )
        
        return {"message": f"Removed {result.modified_count} project relationships"}
    
    elif bulk_data.operation == "update_budget":
        # Bulk update budget allocation
        budget_amount = bulk_data.operation_data.get("budget_amount", 0)
        
        result = await portfolio_projects_collection.update_many(
            {
                "portfolio_id": bulk_data.portfolio_id,
                "project_id": {"$in": bulk_data.project_ids},
                "tenant_id": current_user["tenant_id"],
                "is_active": True
            },
            {"$set": {
                "allocated_budget": budget_amount,
                "updated_at": datetime.utcnow()
            }}
        )
        
        return {"message": f"Updated budget for {result.modified_count} relationships"}
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid bulk operation"
        )
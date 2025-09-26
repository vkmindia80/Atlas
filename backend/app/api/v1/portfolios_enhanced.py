from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import List, Optional, Dict, Any
from datetime import date, datetime
import io
import csv
import json
from decimal import Decimal

from ...models.portfolio_enhanced import (
    EnhancedPortfolio, EnhancedPortfolioResponse, PortfolioProject, 
    PortfolioProjectResponse, PortfolioSnapshot, PortfolioKPI, PortfolioCapacity
)
from ...models.strategic_objective import (
    StrategicObjective, StrategicObjectiveCreate, StrategicObjectiveUpdate, 
    StrategicObjectiveResponse
)
from ...models.common import Status
from ...core.database import get_database
from ...core.security import get_current_user
from ...models.user import User

router = APIRouter()

@router.get("/", response_model=List[EnhancedPortfolioResponse])
async def get_portfolios(
    skip: int = 0,
    limit: int = 100,
    status: Optional[Status] = None,
    portfolio_type: Optional[str] = None,
    portfolio_manager_id: Optional[str] = None,
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Get all portfolios with filtering"""
    query = {"tenant_id": current_user.tenant_id, "is_active": True}
    
    if status:
        query["status"] = status
    if portfolio_type:
        query["portfolio_type"] = portfolio_type
    if portfolio_manager_id:
        query["portfolio_manager_id"] = portfolio_manager_id
    
    portfolios_collection = db.get_default_database().portfolios
    portfolios = await portfolios_collection.find(query).skip(skip).limit(limit).to_list(None)
    
    # Enhance with project counts
    enhanced_portfolios = []
    for portfolio in portfolios:
        portfolio_projects_collection = db.get_default_database().portfolio_projects
        projects_collection = db.get_default_database().projects
        
        project_count = await portfolio_projects_collection.count_documents({
            "portfolio_id": portfolio["id"], 
            "is_active": True
        })
        
        active_project_count = await projects_collection.count_documents({
            "portfolio_id": portfolio["id"],
            "status": "active",
            "is_active": True
        })
        
        portfolio_response = EnhancedPortfolioResponse(
            **portfolio,
            project_count=project_count,
            active_project_count=active_project_count
        )
        enhanced_portfolios.append(portfolio_response)
    
    return enhanced_portfolios

@router.post("/", response_model=EnhancedPortfolioResponse)
async def create_portfolio(
    portfolio_data: Dict[str, Any],
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Create a new portfolio"""
    # Check if portfolio code is unique within tenant
    portfolios_collection = db.get_default_database().portfolios
    existing = await portfolios_collection.find_one({
        "tenant_id": current_user.tenant_id,
        "code": portfolio_data["code"],
        "is_active": True
    })
    if existing:
        raise HTTPException(status_code=400, detail="Portfolio code already exists")
    
    portfolio = EnhancedPortfolio(
        **portfolio_data,
        tenant_id=current_user.tenant_id,
        created_by=current_user.id
    )
    
    result = await db.portfolios.insert_one(portfolio.dict(by_alias=True))
    portfolio.id = result.inserted_id
    
    return EnhancedPortfolioResponse(**portfolio.dict(), project_count=0, active_project_count=0)

@router.get("/{portfolio_id}", response_model=EnhancedPortfolioResponse)
async def get_portfolio(
    portfolio_id: str,
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Get specific portfolio"""
    portfolio = await db.portfolios.find_one({
        "id": portfolio_id,
        "tenant_id": current_user.tenant_id,
        "is_active": True
    })
    
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    # Get project counts
    project_count = await db.portfolio_projects.count_documents({
        "portfolio_id": portfolio_id, 
        "is_active": True
    })
    
    active_project_count = await db.projects.count_documents({
        "portfolio_id": portfolio_id,
        "status": "active",
        "is_active": True
    })
    
    return EnhancedPortfolioResponse(
        **portfolio,
        project_count=project_count,
        active_project_count=active_project_count
    )

@router.put("/{portfolio_id}", response_model=EnhancedPortfolioResponse)
async def update_portfolio(
    portfolio_id: str,
    portfolio_data: Dict[str, Any],
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Update portfolio"""
    portfolio = await db.portfolios.find_one({
        "id": portfolio_id,
        "tenant_id": current_user.tenant_id,
        "is_active": True
    })
    
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    update_data = {k: v for k, v in portfolio_data.items() if v is not None}
    update_data["updated_by"] = current_user.id
    update_data["updated_at"] = datetime.utcnow()
    
    await db.portfolios.update_one(
        {"id": portfolio_id, "tenant_id": current_user.tenant_id},
        {"$set": update_data}
    )
    
    updated_portfolio = await db.portfolios.find_one({
        "id": portfolio_id,
        "tenant_id": current_user.tenant_id
    })
    
    # Get project counts
    project_count = await db.portfolio_projects.count_documents({
        "portfolio_id": portfolio_id, 
        "is_active": True
    })
    
    return EnhancedPortfolioResponse(**updated_portfolio, project_count=project_count)

@router.delete("/{portfolio_id}")
async def delete_portfolio(
    portfolio_id: str,
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Soft delete portfolio"""
    result = await db.portfolios.update_one(
        {"id": portfolio_id, "tenant_id": current_user.tenant_id},
        {"$set": {"is_active": False, "updated_by": current_user.id}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    return {"message": "Portfolio deleted successfully"}

@router.get("/{portfolio_id}/projects", response_model=List[PortfolioProjectResponse])
async def get_portfolio_projects(
    portfolio_id: str,
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Get all projects in a portfolio"""
    pipeline = [
        {
            "$match": {
                "portfolio_id": portfolio_id,
                "tenant_id": current_user.tenant_id,
                "is_active": True
            }
        },
        {
            "$lookup": {
                "from": "projects",
                "localField": "project_id",
                "foreignField": "id",
                "as": "project"
            }
        },
        {
            "$unwind": "$project"
        }
    ]
    
    portfolio_projects = await db.portfolio_projects.aggregate(pipeline).to_list(None)
    
    return [
        PortfolioProjectResponse(
            id=pp["id"],
            portfolio_id=pp["portfolio_id"],
            project_id=pp["project_id"],
            project_name=pp["project"]["name"],
            project_status=pp["project"]["status"],
            strategic_weight=pp["strategic_weight"],
            budget_allocation=pp.get("budget_allocation"),
            priority_ranking=pp.get("priority_ranking"),
            alignment_scores=pp.get("alignment_scores", {}),
            added_date=pp["added_date"]
        )
        for pp in portfolio_projects
    ]

@router.post("/{portfolio_id}/projects/{project_id}")
async def add_project_to_portfolio(
    portfolio_id: str,
    project_id: str,
    relationship_data: Dict[str, Any] = {},
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Add project to portfolio"""
    # Verify portfolio and project exist
    portfolio = await db.portfolios.find_one({
        "id": portfolio_id,
        "tenant_id": current_user.tenant_id,
        "is_active": True
    })
    
    project = await db.projects.find_one({
        "id": project_id,
        "tenant_id": current_user.tenant_id,
        "is_active": True
    })
    
    if not portfolio or not project:
        raise HTTPException(status_code=404, detail="Portfolio or project not found")
    
    # Check if relationship already exists
    existing = await db.portfolio_projects.find_one({
        "portfolio_id": portfolio_id,
        "project_id": project_id,
        "is_active": True
    })
    
    if existing:
        raise HTTPException(status_code=400, detail="Project already in portfolio")
    
    portfolio_project = PortfolioProject(
        portfolio_id=portfolio_id,
        project_id=project_id,
        tenant_id=current_user.tenant_id,
        created_by=current_user.id,
        **relationship_data
    )
    
    await db.portfolio_projects.insert_one(portfolio_project.dict(by_alias=True))
    
    # Update project's portfolio_id
    await db.projects.update_one(
        {"id": project_id, "tenant_id": current_user.tenant_id},
        {"$set": {"portfolio_id": portfolio_id}}
    )
    
    return {"message": "Project added to portfolio successfully"}

@router.delete("/{portfolio_id}/projects/{project_id}")
async def remove_project_from_portfolio(
    portfolio_id: str,
    project_id: str,
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Remove project from portfolio"""
    result = await db.portfolio_projects.update_one(
        {
            "portfolio_id": portfolio_id,
            "project_id": project_id,
            "tenant_id": current_user.tenant_id
        },
        {
            "$set": {
                "is_active": False,
                "updated_by": current_user.id,
                "removed_date": date.today()
            }
        }
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Project not found in portfolio")
    
    # Remove project's portfolio_id
    await db.projects.update_one(
        {"id": project_id, "tenant_id": current_user.tenant_id},
        {"$unset": {"portfolio_id": ""}}
    )
    
    return {"message": "Project removed from portfolio successfully"}

@router.get("/{portfolio_id}/dashboard")
async def get_portfolio_dashboard(
    portfolio_id: str,
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Get portfolio dashboard data with KPIs"""
    portfolio = await db.portfolios.find_one({
        "id": portfolio_id,
        "tenant_id": current_user.tenant_id,
        "is_active": True
    })
    
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    # Get project status counts
    project_status_pipeline = [
        {
            "$match": {
                "portfolio_id": portfolio_id,
                "tenant_id": current_user.tenant_id,
                "is_active": True
            }
        },
        {
            "$group": {
                "_id": "$status",
                "count": {"$sum": 1}
            }
        }
    ]
    
    status_counts = await db.projects.aggregate(project_status_pipeline).to_list(None)
    status_summary = {item["_id"]: item["count"] for item in status_counts}
    
    # Get budget aggregation
    budget_pipeline = [
        {
            "$match": {
                "portfolio_id": portfolio_id,
                "tenant_id": current_user.tenant_id,
                "is_active": True
            }
        },
        {
            "$group": {
                "_id": None,
                "total_budget": {"$sum": "$financials.total_budget"},
                "total_spent": {"$sum": "$financials.spent_amount"},
                "total_committed": {"$sum": "$financials.committed_amount"}
            }
        }
    ]
    
    budget_data = await db.projects.aggregate(budget_pipeline).to_list(None)
    budget_summary = budget_data[0] if budget_data else {
        "total_budget": 0,
        "total_spent": 0,
        "total_committed": 0
    }
    
    # Get risk heatmap data
    risk_pipeline = [
        {
            "$match": {
                "portfolio_id": portfolio_id,
                "tenant_id": current_user.tenant_id,
                "is_active": True
            }
        },
        {
            "$group": {
                "_id": "$health_status",
                "count": {"$sum": 1},
                "avg_risk_score": {"$avg": "$risk_score"}
            }
        }
    ]
    
    risk_data = await db.projects.aggregate(risk_pipeline).to_list(None)
    risk_heatmap = {item["_id"]: {"count": item["count"], "avg_risk": item["avg_risk_score"]} for item in risk_data}
    
    return {
        "portfolio": EnhancedPortfolioResponse(**portfolio),
        "kpis": {
            "status_counts": status_summary,
            "budget_summary": budget_summary,
            "risk_heatmap": risk_heatmap,
            "total_projects": sum(status_summary.values()),
            "budget_utilization_percentage": (
                float(budget_summary["total_spent"]) / float(budget_summary["total_budget"]) * 100
                if budget_summary["total_budget"] > 0 else 0
            )
        }
    }

@router.post("/{portfolio_id}/snapshots")
async def create_portfolio_snapshot(
    portfolio_id: str,
    snapshot_data: Dict[str, Any],
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Create portfolio performance snapshot"""
    portfolio = await db.portfolios.find_one({
        "id": portfolio_id,
        "tenant_id": current_user.tenant_id,
        "is_active": True
    })
    
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    # Calculate snapshot metrics
    projects = await db.projects.find({
        "portfolio_id": portfolio_id,
        "tenant_id": current_user.tenant_id,
        "is_active": True
    }).to_list(None)
    
    total_projects = len(projects)
    active_projects = len([p for p in projects if p["status"] == "active"])
    completed_projects = len([p for p in projects if p["status"] == "completed"])
    on_hold_projects = len([p for p in projects if p["status"] == "on_hold"])
    cancelled_projects = len([p for p in projects if p["status"] == "cancelled"])
    
    projects_on_track = len([p for p in projects if p["health_status"] == "green"])
    projects_at_risk = len([p for p in projects if p["health_status"] == "yellow"])
    projects_critical = len([p for p in projects if p["health_status"] == "red"])
    
    snapshot = PortfolioSnapshot(
        portfolio_id=portfolio_id,
        created_by=current_user.id,
        tenant_id=current_user.tenant_id,
        financial_snapshot=portfolio["financial_metrics"],
        total_projects=total_projects,
        active_projects=active_projects,
        completed_projects=completed_projects,
        on_hold_projects=on_hold_projects,
        cancelled_projects=cancelled_projects,
        projects_on_track=projects_on_track,
        projects_at_risk=projects_at_risk,
        projects_critical=projects_critical,
        **snapshot_data
    )
    
    await db.portfolio_snapshots.insert_one(snapshot.dict(by_alias=True))
    
    return {"message": "Portfolio snapshot created successfully", "snapshot_id": snapshot.id}

# Strategic Objectives endpoints
@router.get("/objectives/", response_model=List[StrategicObjectiveResponse])
async def get_strategic_objectives(
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Get all strategic objectives"""
    objectives = await db.strategic_objectives.find({
        "tenant_id": current_user.tenant_id,
        "is_active": True
    }).to_list(None)
    
    return [StrategicObjectiveResponse(**obj) for obj in objectives]

@router.post("/objectives/", response_model=StrategicObjectiveResponse)
async def create_strategic_objective(
    objective_data: StrategicObjectiveCreate,
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Create strategic objective"""
    objective = StrategicObjective(
        **objective_data.dict(),
        tenant_id=current_user.tenant_id,
        created_by=current_user.id
    )
    
    await db.strategic_objectives.insert_one(objective.dict(by_alias=True))
    
    return StrategicObjectiveResponse(**objective.dict())

@router.put("/objectives/{objective_id}", response_model=StrategicObjectiveResponse)
async def update_strategic_objective(
    objective_id: str,
    objective_data: StrategicObjectiveUpdate,
    db=Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Update strategic objective"""
    update_data = {k: v for k, v in objective_data.dict().items() if v is not None}
    update_data["updated_by"] = current_user.id
    update_data["updated_at"] = datetime.utcnow()
    
    result = await db.strategic_objectives.update_one(
        {"id": objective_id, "tenant_id": current_user.tenant_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Strategic objective not found")
    
    updated_objective = await db.strategic_objectives.find_one({
        "id": objective_id,
        "tenant_id": current_user.tenant_id
    })
    
    return StrategicObjectiveResponse(**updated_objective)
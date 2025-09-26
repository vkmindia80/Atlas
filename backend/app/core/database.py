from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import IndexModel, ASCENDING
from .config import settings
import asyncio
from typing import Optional

class Database:
    client: Optional[AsyncIOMotorClient] = None
    
db = Database()

async def get_database() -> AsyncIOMotorClient:
    return db.client

async def connect_to_mongo():
    """Create database connection"""
    db.client = AsyncIOMotorClient(settings.MONGO_URL)
    
    # Create indexes for multi-tenancy and performance
    database = db.client.get_default_database()
    
    # Users collection indexes
    users_collection = database.users
    await users_collection.create_indexes([
        IndexModel([("email", ASCENDING), ("tenant_id", ASCENDING)], unique=True),
        IndexModel([("tenant_id", ASCENDING)]),
        IndexModel([("username", ASCENDING), ("tenant_id", ASCENDING)], unique=True)
    ])
    
    # Portfolios collection indexes
    portfolios_collection = database.portfolios
    await portfolios_collection.create_indexes([
        IndexModel([("tenant_id", ASCENDING)]),
        IndexModel([("code", ASCENDING), ("tenant_id", ASCENDING)], unique=True),
        IndexModel([("created_by", ASCENDING)]),
        IndexModel([("status", ASCENDING)])
    ])
    
    # Projects collection indexes
    projects_collection = database.projects
    await projects_collection.create_indexes([
        IndexModel([("tenant_id", ASCENDING)]),
        IndexModel([("code", ASCENDING), ("tenant_id", ASCENDING)], unique=True),
        IndexModel([("portfolio_id", ASCENDING)]),
        IndexModel([("project_manager_id", ASCENDING)]),
        IndexModel([("status", ASCENDING)]),
        IndexModel([("start_date", ASCENDING)]),
        IndexModel([("end_date", ASCENDING)])
    ])
    
    # Tenants collection indexes
    tenants_collection = database.tenants
    await tenants_collection.create_indexes([
        IndexModel([("code", ASCENDING)], unique=True),
        IndexModel([("domain", ASCENDING)], unique=True),
        IndexModel([("status", ASCENDING)])
    ])
    
    # Tasks collection indexes
    tasks_collection = database.tasks
    await tasks_collection.create_indexes([
        IndexModel([("tenant_id", ASCENDING)]),
        IndexModel([("project_id", ASCENDING)]),
        IndexModel([("status", ASCENDING)]),
        IndexModel([("priority", ASCENDING)]),
        IndexModel([("planned_start_date", ASCENDING)]),
        IndexModel([("planned_end_date", ASCENDING)]),
        IndexModel([("assignments.user_id", ASCENDING)])
    ])
    
    # Portfolio projects relationship indexes
    portfolio_projects_collection = database.portfolio_projects
    await portfolio_projects_collection.create_indexes([
        IndexModel([("tenant_id", ASCENDING)]),
        IndexModel([("portfolio_id", ASCENDING)]),
        IndexModel([("project_id", ASCENDING)]),
        IndexModel([("portfolio_id", ASCENDING), ("project_id", ASCENDING)], unique=True),
        IndexModel([("relationship_type", ASCENDING)])
    ])
    
    # Project templates indexes
    project_templates_collection = database.project_templates
    await project_templates_collection.create_indexes([
        IndexModel([("tenant_id", ASCENDING)]),
        IndexModel([("project_type", ASCENDING)]),
        IndexModel([("is_active", ASCENDING)])
    ])
    
    # Project intake forms indexes
    project_intake_collection = database.project_intake_forms
    await project_intake_collection.create_indexes([
        IndexModel([("tenant_id", ASCENDING)]),
        IndexModel([("requestor_id", ASCENDING)]),
        IndexModel([("status", ASCENDING)]),
        IndexModel([("project_type", ASCENDING)])
    ])
    
    # Project snapshots indexes
    project_snapshots_collection = database.project_snapshots
    await project_snapshots_collection.create_indexes([
        IndexModel([("tenant_id", ASCENDING)]),
        IndexModel([("project_id", ASCENDING)]),
        IndexModel([("snapshot_date", ASCENDING)]),
        IndexModel([("snapshot_type", ASCENDING)])
    ])

async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
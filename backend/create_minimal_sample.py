#!/usr/bin/env python3
"""
Simple script to create minimal sample data for testing
"""
import asyncio
import uuid
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient

async def create_minimal_data():
    # Connect to MongoDB
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.atlaspm_dev
    
    # Create a test tenant
    tenant_id = str(uuid.uuid4())
    await db.tenants.insert_one({
        "_id": tenant_id,
        "name": "Demo Organization",
        "code": "DEMO",
        "created_at": datetime.utcnow(),
        "is_active": True
    })
    
    # Create a test user
    user_id = str(uuid.uuid4())
    await db.users.insert_one({
        "_id": user_id,
        "tenant_id": tenant_id,
        "username": "demo",
        "email": "demo@example.com",
        "full_name": "Demo User",
        "role": "project_manager",
        "is_active": True,
        "created_at": datetime.utcnow()
    })
    
    # Create a test portfolio
    portfolio_id = str(uuid.uuid4())
    await db.portfolios.insert_one({
        "_id": portfolio_id,
        "tenant_id": tenant_id,
        "name": "Digital Transformation Portfolio",
        "code": "DT2024",
        "description": "Enterprise digital transformation initiatives",
        "portfolio_type": "strategic",
        "status": "active",
        "health_status": "green",
        "priority": "high",
        "portfolio_manager_id": user_id,
        "created_at": datetime.utcnow()
    })
    
    # Create sample projects with tasks
    projects_data = [
        {
            "name": "Customer Portal Modernization",
            "code": "CPM-2024",
            "description": "Modernize legacy customer portal with React and microservices architecture",
            "project_type": "software_development",
            "methodology": "agile"
        },
        {
            "name": "Cloud Infrastructure Migration", 
            "code": "CIM-2024",
            "description": "Migrate on-premise infrastructure to AWS cloud platform",
            "project_type": "infrastructure",
            "methodology": "waterfall"
        }
    ]
    
    project_ids = []
    for i, project_data in enumerate(projects_data):
        project_id = str(uuid.uuid4())
        project_ids.append(project_id)
        
        # Create sample tasks for this project
        tasks = []
        task_names = [
            "Requirements Analysis",
            "System Design", 
            "Frontend Development",
            "Backend API Development",
            "Database Schema Design",
            "Integration Testing",
            "User Acceptance Testing",
            "Production Deployment"
        ]
        
        for j, task_name in enumerate(task_names):
            task_id = str(uuid.uuid4())
            start_date = datetime.utcnow() + timedelta(days=j*5)
            end_date = start_date + timedelta(days=random.choice([3, 5, 7, 10]))
            
            tasks.append({
                "id": task_id,
                "name": task_name,
                "description": f"Complete {task_name.lower()} for the project",
                "status": random.choice(["not_started", "in_progress", "completed"]),
                "priority": random.choice(["low", "medium", "high"]),
                "assignee_id": user_id,
                "planned_start_date": start_date.isoformat(),
                "planned_end_date": end_date.isoformat(),
                "estimated_hours": random.randint(20, 80),
                "percent_complete": random.randint(0, 100),
                "subtasks": [],
                "dependencies": [],
                "labels": random.sample(["frontend", "backend", "testing", "deployment", "analysis"], 2),
                "tags": []
            })
        
        # Create sample milestones
        milestones = [
            {
                "id": str(uuid.uuid4()),
                "name": "Project Kickoff",
                "planned_date": datetime.utcnow().isoformat(),
                "status": "completed"
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Design Review",
                "planned_date": (datetime.utcnow() + timedelta(days=30)).isoformat(),
                "status": "in_progress"
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Go Live",
                "planned_date": (datetime.utcnow() + timedelta(days=90)).isoformat(),
                "status": "not_started"
            }
        ]
        
        project_doc = {
            "_id": project_id,
            "tenant_id": tenant_id,
            **project_data,
            "status": "active",
            "health_status": random.choice(["green", "yellow"]),
            "priority": random.choice(["medium", "high"]),
            "portfolio_id": portfolio_id,
            "project_manager_id": user_id,
            "sponsor_id": user_id,
            "team_members": [user_id],
            "planned_start_date": datetime.utcnow().isoformat(),
            "planned_end_date": (datetime.utcnow() + timedelta(days=120)).isoformat(),
            "actual_start_date": datetime.utcnow().isoformat(),
            "actual_end_date": None,
            "percent_complete": random.randint(25, 75),
            "milestones": milestones,
            "tasks": tasks,
            "risks": [],
            "issues": [],
            "financials": {
                "total_budget": 250000,
                "allocated_budget": 200000,
                "spent_amount": 125000,
                "committed_amount": 50000,
                "forecasted_cost": 225000,
                "budget_variance": -25000,
                "cost_to_complete": 100000,
                "labor_cost": 150000,
                "material_cost": 30000,
                "vendor_cost": 45000,
                "overhead_cost": 25000
            },
            "resource_allocations": [],
            "risk_score": random.randint(1, 5),
            "open_issues_count": random.randint(0, 3),
            "open_risks_count": random.randint(0, 2),
            "document_urls": [],
            "custom_fields": {},
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "created_by": user_id,
            "is_active": True,
            "metadata": {}
        }
        
        await db.projects.insert_one(project_doc)
    
    print(f"Created sample data:")
    print(f"- Tenant ID: {tenant_id}")
    print(f"- User ID: {user_id}")
    print(f"- Portfolio ID: {portfolio_id}")
    print(f"- Project IDs: {project_ids}")
    
    client.close()

if __name__ == "__main__":
    import random
    asyncio.run(create_minimal_data())
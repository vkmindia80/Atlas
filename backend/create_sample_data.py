#!/usr/bin/env python3
"""
Script to create realistic sample data for AtlasPM
Generates portfolios, projects, tasks, and relationships
"""

import asyncio
import uuid
from datetime import datetime, date, timedelta
from decimal import Decimal
from motor.motor_asyncio import AsyncIOMotorClient
import random

# Sample data constants
PROJECT_TYPES = ["software_development", "infrastructure", "research", "marketing", "process_improvement"]
METHODOLOGIES = ["agile", "waterfall", "scrum", "kanban", "hybrid"]
STATUSES = ["draft", "active", "on_hold", "completed", "cancelled"]
PRIORITIES = ["low", "medium", "high", "critical"]
HEALTH_STATUSES = ["green", "yellow", "red"]

# Sample project names and descriptions
PROJECT_TEMPLATES = [
    {
        "name": "Customer Portal Modernization",
        "description": "Modernize legacy customer portal with React and microservices architecture",
        "type": "software_development",
        "methodology": "agile",
        "budget_range": (150000, 300000),
        "duration_months": 8
    },
    {
        "name": "Data Center Migration",
        "description": "Migrate on-premise data center to cloud infrastructure",
        "type": "infrastructure", 
        "methodology": "waterfall",
        "budget_range": (500000, 800000),
        "duration_months": 12
    },
    {
        "name": "AI-Powered Analytics Platform",
        "description": "Develop machine learning platform for predictive analytics",
        "type": "software_development",
        "methodology": "scrum",
        "budget_range": (200000, 400000),
        "duration_months": 10
    },
    {
        "name": "Digital Marketing Campaign",
        "description": "Multi-channel digital marketing campaign for Q4 product launch",
        "type": "marketing",
        "methodology": "kanban",
        "budget_range": (75000, 150000),
        "duration_months": 4
    },
    {
        "name": "ERP System Implementation",
        "description": "Implementation of new enterprise resource planning system",
        "type": "software_development",
        "methodology": "hybrid",
        "budget_range": (600000, 1000000),
        "duration_months": 18
    },
    {
        "name": "Cybersecurity Framework Enhancement",
        "description": "Strengthen cybersecurity posture with new framework and tools",
        "type": "infrastructure",
        "methodology": "agile",
        "budget_range": (100000, 200000),
        "duration_months": 6
    },
    {
        "name": "Mobile App Development",
        "description": "Native mobile application for iOS and Android platforms",
        "type": "software_development",
        "methodology": "scrum",
        "budget_range": (120000, 250000),
        "duration_months": 9
    },
    {
        "name": "Business Process Automation",
        "description": "Automate manual business processes using RPA technology",
        "type": "process_improvement",
        "methodology": "lean",
        "budget_range": (80000, 160000),
        "duration_months": 5
    },
    {
        "name": "Cloud-Native Architecture Migration",
        "description": "Migrate legacy applications to cloud-native architecture",
        "type": "infrastructure",
        "methodology": "agile",
        "budget_range": (300000, 500000),
        "duration_months": 14
    },
    {
        "name": "Supply Chain Optimization Research",
        "description": "Research project to optimize supply chain efficiency using AI",
        "type": "research",
        "methodology": "waterfall",
        "budget_range": (90000, 180000),
        "duration_months": 7
    }
]

PORTFOLIO_TEMPLATES = [
    {
        "name": "Digital Transformation Initiative",
        "description": "Strategic portfolio focused on digital transformation across the organization",
        "type": "strategic",
        "budget": 2000000
    },
    {
        "name": "Operational Excellence Program",
        "description": "Portfolio aimed at improving operational efficiency and reducing costs",
        "type": "operational", 
        "budget": 1500000
    },
    {
        "name": "Innovation Lab Projects",
        "description": "Research and development portfolio for emerging technologies",
        "type": "innovation",
        "budget": 800000
    }
]

TASK_TEMPLATES = [
    "Requirements Gathering", "System Architecture Design", "Database Schema Design",
    "Frontend Development", "Backend API Development", "Integration Testing",
    "User Acceptance Testing", "Security Assessment", "Performance Testing",
    "Documentation", "Deployment Planning", "Go-Live Preparation"
]

async def create_sample_tenant(client):
    """Create sample tenant"""
    db = client.get_default_database()
    tenants_collection = db.tenants
    
    tenant_id = str(uuid.uuid4())
    tenant_doc = {
        "_id": tenant_id,
        "name": "Acme Corporation",
        "code": "ACME",
        "domain": "acme.com",
        "status": "active",
        "subscription_type": "enterprise",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "is_active": True,
        "metadata": {}
    }
    
    await tenants_collection.insert_one(tenant_doc)
    return tenant_id

async def create_sample_users(client, tenant_id):
    """Create sample users"""
    db = client.get_default_database()
    users_collection = db.users
    
    users = []
    
    # Create admin user
    admin_id = str(uuid.uuid4())
    admin_doc = {
        "_id": admin_id,
        "tenant_id": tenant_id,
        "username": "admin",
        "email": "admin@acme.com",
        "first_name": "System",
        "last_name": "Administrator",
        "role": "admin",
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "metadata": {}
    }
    users.append(admin_doc)
    
    # Create PMO users
    pmo_users = [
        {"name": "Sarah Johnson", "email": "sarah.johnson@acme.com", "role": "pmo_admin"},
        {"name": "Michael Chen", "email": "michael.chen@acme.com", "role": "portfolio_manager"},
    ]
    
    for user_data in pmo_users:
        user_id = str(uuid.uuid4())
        names = user_data["name"].split()
        user_doc = {
            "_id": user_id,
            "tenant_id": tenant_id,
            "username": user_data["email"].split("@")[0],
            "email": user_data["email"],
            "first_name": names[0],
            "last_name": names[1],
            "role": user_data["role"],
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "metadata": {}
        }
        users.append(user_doc)
    
    # Create project managers
    pm_users = [
        "Alice Rodriguez", "David Kim", "Emma Thompson", "James Wilson", "Lisa Chen"
    ]
    
    for name in pm_users:
        user_id = str(uuid.uuid4())
        names = name.split()
        email = f"{names[0].lower()}.{names[1].lower()}@acme.com"
        user_doc = {
            "_id": user_id,
            "tenant_id": tenant_id,
            "username": email.split("@")[0],
            "email": email,
            "first_name": names[0],
            "last_name": names[1],
            "role": "project_manager",
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "metadata": {}
        }
        users.append(user_doc)
    
    await users_collection.insert_many(users)
    return [user["_id"] for user in users]

async def create_sample_portfolios(client, tenant_id, user_ids):
    """Create sample portfolios"""
    db = client.get_default_database()
    portfolios_collection = db.portfolios
    
    portfolios = []
    
    for i, portfolio_template in enumerate(PORTFOLIO_TEMPLATES):
        portfolio_id = str(uuid.uuid4())
        portfolio_doc = {
            "_id": portfolio_id,
            "tenant_id": tenant_id,
            "name": portfolio_template["name"],
            "code": f"PF{i+1:03d}",
            "description": portfolio_template["description"],
            "portfolio_type": portfolio_template["type"],
            "status": "active",
            "health_status": random.choice(HEALTH_STATUSES),
            "priority": random.choice(PRIORITIES),
            "portfolio_manager_id": random.choice(user_ids[2:4]),  # PMO users
            "sponsors": [random.choice(user_ids[1:3])],
            "stakeholders": random.sample(user_ids[2:], 2),
            "strategic_objectives": [],
            "business_case_url": None,
            "start_date": (date.today() - timedelta(days=random.randint(30, 365))).isoformat(),
            "end_date": (date.today() + timedelta(days=random.randint(180, 730))).isoformat(),
            "financial_metrics": {
                "total_budget": portfolio_template["budget"],
                "allocated_budget": portfolio_template["budget"] * 0.8,
                "spent_amount": portfolio_template["budget"] * random.uniform(0.1, 0.6),
                "committed_amount": portfolio_template["budget"] * random.uniform(0.6, 0.8),
                "forecasted_cost": portfolio_template["budget"] * random.uniform(0.9, 1.1)
            },
            "risk_metrics": {
                "risk_score": random.uniform(0.1, 0.8),
                "high_risks_count": random.randint(0, 3),
                "medium_risks_count": random.randint(2, 8),
                "low_risks_count": random.randint(5, 15),
                "overdue_risks_count": random.randint(0, 2)
            },
            "project_ids": [],
            "settings": {},
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "created_by": user_ids[0],
            "is_active": True,
            "metadata": {}
        }
        portfolios.append(portfolio_doc)
    
    await portfolios_collection.insert_many(portfolios)
    return [portfolio["_id"] for portfolio in portfolios]

async def create_sample_projects(client, tenant_id, user_ids, portfolio_ids):
    """Create sample projects"""
    db = client.get_default_database()
    projects_collection = db.projects
    
    projects = []
    
    for i, project_template in enumerate(PROJECT_TEMPLATES):
        project_id = str(uuid.uuid4())
        
        # Calculate dates
        start_date = date.today() - timedelta(days=random.randint(30, 180))
        end_date = start_date + timedelta(days=project_template["duration_months"] * 30)
        actual_start = start_date + timedelta(days=random.randint(-5, 15))
        
        # Calculate budget
        budget = random.randint(*project_template["budget_range"])
        spent_percentage = random.uniform(0.1, 0.7)
        
        project_doc = {
            "_id": project_id,
            "tenant_id": tenant_id,
            "name": project_template["name"],
            "code": f"PRJ{i+1:03d}",
            "description": project_template["description"],
            "project_type": project_template["type"],
            "methodology": project_template["methodology"],
            "status": random.choice(["draft", "active", "active", "active", "completed"]),  # Bias toward active
            "health_status": random.choice(HEALTH_STATUSES),
            "priority": random.choice(PRIORITIES),
            "portfolio_id": random.choice(portfolio_ids),
            "parent_project_id": None,
            "project_manager_id": random.choice(user_ids[4:]),  # PM users
            "sponsor_id": random.choice(user_ids[1:4]),
            "team_members": random.sample(user_ids[4:], random.randint(3, 6)),
            "planned_start_date": start_date,
            "planned_end_date": end_date,
            "actual_start_date": actual_start,
            "actual_end_date": None if random.choice([True, False]) else end_date + timedelta(days=random.randint(-10, 30)),
            "percent_complete": random.uniform(10, 95) if i < 8 else 100,
            "milestones": [],
            "financials": {
                "total_budget": budget,
                "allocated_budget": budget,
                "spent_amount": budget * spent_percentage,
                "committed_amount": budget * (spent_percentage + random.uniform(0.1, 0.3)),
                "forecasted_cost": budget * random.uniform(0.9, 1.1),
                "budget_variance": budget * random.uniform(-0.1, 0.2),
                "cost_to_complete": budget * (1 - spent_percentage),
                "labor_cost": budget * 0.6,
                "material_cost": budget * 0.2,
                "vendor_cost": budget * 0.15,
                "overhead_cost": budget * 0.05
            },
            "resource_allocations": [],
            "risk_score": random.uniform(0.1, 0.8),
            "open_issues_count": random.randint(0, 8),
            "open_risks_count": random.randint(1, 12),
            "document_urls": [],
            "custom_fields": {},
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "created_by": user_ids[0],
            "is_active": True,
            "metadata": {}
        }
        projects.append(project_doc)
    
    await projects_collection.insert_many(projects)
    return [project["_id"] for project in projects]

async def create_sample_tasks(client, tenant_id, user_ids, project_ids):
    """Create sample tasks for projects"""
    db = client.get_default_database()
    tasks_collection = db.tasks
    
    tasks = []
    task_statuses = ["todo", "in_progress", "in_review", "done"]
    
    for project_id in project_ids:
        # Create 8-15 tasks per project
        num_tasks = random.randint(8, 15)
        
        for i in range(num_tasks):
            task_id = str(uuid.uuid4())
            task_name = random.choice(TASK_TEMPLATES)
            
            # Add project-specific context to task name
            if i < len(TASK_TEMPLATES):
                task_name = TASK_TEMPLATES[i]
            else:
                task_name = f"{random.choice(TASK_TEMPLATES)} - Phase {(i // len(TASK_TEMPLATES)) + 1}"
            
            start_date = date.today() - timedelta(days=random.randint(0, 90))
            end_date = start_date + timedelta(days=random.randint(3, 21))
            
            task_doc = {
                "_id": task_id,
                "tenant_id": tenant_id,
                "name": task_name,
                "description": f"Detailed task for {task_name.lower()}",
                "task_type": random.choice(["story", "task", "task", "bug"]),
                "status": random.choice(task_statuses),
                "priority": random.choice(PRIORITIES),
                "project_id": project_id,
                "parent_task_id": None,
                "milestone_id": None,
                "assignments": [],
                "planned_start_date": start_date,
                "planned_end_date": end_date,
                "actual_start_date": start_date if random.choice([True, False]) else None,
                "actual_end_date": end_date if random.choice([True, False]) else None,
                "estimated_hours": random.randint(4, 40),
                "remaining_hours": random.randint(0, 20),
                "percent_complete": random.uniform(0, 100),
                "dependencies": [],
                "time_entries": [],
                "labels": random.sample(["frontend", "backend", "database", "testing", "documentation"], 2),
                "tags": random.sample(["critical", "enhancement", "bug", "feature"], 1),
                "story_points": random.choice([1, 2, 3, 5, 8, 13]),
                "business_value": random.randint(1, 100),
                "board_column": random.choice(["todo", "in_progress", "review", "done"]),
                "board_position": i,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "created_by": random.choice(user_ids),
                "is_active": True,
                "metadata": {}
            }
            tasks.append(task_doc)
    
    await tasks_collection.insert_many(tasks)
    return len(tasks)

async def create_portfolio_project_relationships(client, tenant_id, portfolio_ids, project_ids, user_ids):
    """Create portfolio-project relationships"""
    db = client.get_default_database()
    portfolio_projects_collection = db.portfolio_projects
    
    relationships = []
    
    # Distribute projects across portfolios
    for i, project_id in enumerate(project_ids):
        portfolio_id = portfolio_ids[i % len(portfolio_ids)]
        
        relationship_id = str(uuid.uuid4())
        relationship_doc = {
            "_id": relationship_id,
            "tenant_id": tenant_id,
            "portfolio_id": portfolio_id,
            "project_id": project_id,
            "relationship_type": "primary",
            "status": "active",
            "allocated_budget": random.randint(50000, 500000),
            "budget_percentage": random.uniform(10, 30),
            "strategic_objective_ids": [],
            "alignment_score": random.uniform(0.6, 1.0),
            "contribution_weight": random.uniform(0.8, 1.2),
            "portfolio_phase": f"Phase {random.randint(1, 3)}",
            "expected_value_delivery_date": date.today() + timedelta(days=random.randint(30, 365)),
            "resource_rules": {
                "max_budget_percentage": None,
                "max_team_size": None,
                "priority_multiplier": 1.0
            },
            "review_frequency_days": 30,
            "last_review_date": datetime.utcnow() - timedelta(days=random.randint(1, 30)),
            "next_review_date": datetime.utcnow() + timedelta(days=random.randint(1, 30)),
            "value_delivered": random.randint(10000, 100000),
            "roi_calculation": random.uniform(0.1, 0.4),
            "risk_adjusted_value": None,
            "dependent_project_ids": [],
            "dependency_project_ids": [],
            "relationship_notes": f"Strategic project contributing to portfolio objectives",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "created_by": user_ids[0],
            "is_active": True,
            "metadata": {}
        }
        relationships.append(relationship_doc)
    
    await portfolio_projects_collection.insert_many(relationships)
    return len(relationships)

async def main():
    """Main function to create all sample data"""
    print("🚀 Creating AtlasPM sample data...")
    
    # Connect to MongoDB
    client = AsyncIOMotorClient("mongodb://localhost:27017/atlaspm")
    
    try:
        # Create tenant
        print("📁 Creating sample tenant...")
        tenant_id = await create_sample_tenant(client)
        
        # Create users
        print("👥 Creating sample users...")
        user_ids = await create_sample_users(client, tenant_id)
        print(f"   Created {len(user_ids)} users")
        
        # Create portfolios
        print("📊 Creating sample portfolios...")
        portfolio_ids = await create_sample_portfolios(client, tenant_id, user_ids)
        print(f"   Created {len(portfolio_ids)} portfolios")
        
        # Create projects
        print("🎯 Creating sample projects...")
        project_ids = await create_sample_projects(client, tenant_id, user_ids, portfolio_ids)
        print(f"   Created {len(project_ids)} projects")
        
        # Create tasks
        print("📝 Creating sample tasks...")
        task_count = await create_sample_tasks(client, tenant_id, user_ids, project_ids)
        print(f"   Created {task_count} tasks")
        
        # Create portfolio-project relationships
        print("🔗 Creating portfolio-project relationships...")
        relationship_count = await create_portfolio_project_relationships(
            client, tenant_id, portfolio_ids, project_ids, user_ids
        )
        print(f"   Created {relationship_count} relationships")
        
        print("✅ Sample data creation completed successfully!")
        print(f"   Tenant ID: {tenant_id}")
        print(f"   Access the application at: http://localhost:3000")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {str(e)}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main())
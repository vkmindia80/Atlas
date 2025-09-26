#!/usr/bin/env python3
"""
Add sample portfolios and projects to existing AtlasPM tenant
"""

import asyncio
import uuid
from datetime import datetime, date, timedelta
from decimal import Decimal
from motor.motor_asyncio import AsyncIOMotorClient
import random

# Use the project templates from the original script
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

async def main():
    """Add sample portfolios and projects"""
    print("🚀 Adding AtlasPM sample projects...")
    
    client = AsyncIOMotorClient("mongodb://localhost:27017/atlaspm")
    db = client.get_default_database()
    
    try:
        # Get existing tenant and users
        tenant = await db.tenants.find_one()
        users = await db.users.find({"tenant_id": tenant["_id"]}).to_list(length=None)
        
        if not tenant or not users:
            print("❌ No existing tenant or users found!")
            return
        
        tenant_id = tenant["_id"]
        user_ids = [user["_id"] for user in users]
        
        print(f"📁 Using tenant: {tenant['name']} ({tenant_id})")
        print(f"👥 Found {len(users)} users")
        
        # Create portfolios first
        print("📊 Creating portfolios...")
        portfolios_collection = db.portfolios
        portfolio_ids = []
        
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
                "health_status": random.choice(["green", "yellow", "red"]),
                "priority": random.choice(["low", "medium", "high", "critical"]),
                "portfolio_manager_id": user_ids[2],  # Michael Chen
                "sponsors": [user_ids[1]],  # Sarah Johnson
                "stakeholders": [user_ids[1], user_ids[2]],
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
            
            await portfolios_collection.insert_one(portfolio_doc)
            portfolio_ids.append(portfolio_id)
            print(f"   ✅ Created portfolio: {portfolio_template['name']}")
        
        # Create projects
        print("🎯 Creating projects...")
        projects_collection = db.projects
        project_ids = []
        
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
                "status": random.choice(["draft", "active", "active", "active", "completed"]),
                "health_status": random.choice(["green", "yellow", "red"]),
                "priority": random.choice(["low", "medium", "high", "critical"]),
                "portfolio_id": portfolio_ids[i % len(portfolio_ids)],
                "parent_project_id": None,
                "project_manager_id": user_ids[3 + (i % 5)],  # Rotate through PMs
                "sponsor_id": user_ids[1],  # Sarah Johnson
                "team_members": random.sample(user_ids[3:], random.randint(2, 4)),
                "planned_start_date": start_date.isoformat(),
                "planned_end_date": end_date.isoformat(),
                "actual_start_date": actual_start.isoformat(),
                "actual_end_date": None,
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
            
            await projects_collection.insert_one(project_doc)
            project_ids.append(project_id)
            print(f"   ✅ Created project: {project_template['name']}")
        
        # Create portfolio-project relationships
        print("🔗 Creating portfolio-project relationships...")
        portfolio_projects_collection = db.portfolio_projects
        
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
                "expected_value_delivery_date": (date.today() + timedelta(days=random.randint(30, 365))).isoformat(),
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
            
            await portfolio_projects_collection.insert_one(relationship_doc)
        
        # Update portfolios with project IDs
        for i, portfolio_id in enumerate(portfolio_ids):
            portfolio_project_ids = [project_ids[j] for j in range(len(project_ids)) if j % len(portfolio_ids) == i]
            await portfolios_collection.update_one(
                {"_id": portfolio_id},
                {"$set": {"project_ids": portfolio_project_ids}}
            )
        
        print("✅ Sample data creation completed successfully!")
        print(f"   📊 Created {len(portfolio_ids)} portfolios")
        print(f"   🎯 Created {len(project_ids)} projects")
        print(f"   🔗 Created {len(project_ids)} relationships")
        print("   🌐 Access the application at: http://localhost:3000")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {str(e)}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main())
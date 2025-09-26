#!/usr/bin/env python3
"""
Sample Data Seeder for AtlasPM
Creates 100 sample projects, portfolios, and related data for testing and demonstration
"""

import asyncio
import random
import uuid
from datetime import datetime, date, timedelta
from decimal import Decimal
import os
import sys

# Add the app directory to path so we can import our modules
sys.path.append('/app/backend')

from motor.motor_asyncio import AsyncIOMotorClient
from app.models.portfolio_enhanced import EnhancedPortfolio, PortfolioProject
from app.models.project_enhanced import EnhancedProject, ProjectTask, ProjectRisk, ProjectIssue, Milestone
from app.models.strategic_objective import StrategicObjective, KPI
from app.models.user import User, UserRole, UserStatus
from app.models.tenant import Tenant
from app.core.config import settings
from app.core.security import get_password_hash

# Sample data constants
TENANT_ID = "sample-tenant-001"
SAMPLE_USERS = []
SAMPLE_PORTFOLIOS = []
SAMPLE_PROJECTS = []

PROJECT_TYPES = ["software_development", "infrastructure", "research", "marketing", "process_improvement", "compliance"]
PROJECT_METHODOLOGIES = ["agile", "scrum", "kanban", "waterfall", "hybrid"]
STATUSES = ["draft", "active", "on_hold", "completed", "cancelled"]
HEALTH_STATUSES = ["green", "yellow", "red"]
PRIORITIES = ["low", "medium", "high", "critical"]

# Project name templates
PROJECT_NAMES = [
    "Digital Transformation Platform", "Customer Portal Redesign", "Mobile App Development",
    "Cloud Migration Initiative", "Data Analytics Platform", "Security Enhancement Program",
    "E-commerce Integration", "API Gateway Implementation", "DevOps Automation",
    "Legacy System Modernization", "Microservices Architecture", "AI/ML Integration Platform",
    "Real-time Analytics Dashboard", "Multi-tenant SaaS Platform", "Identity Management System",
    "Content Management System", "Payment Gateway Integration", "Inventory Management System",
    "Customer Relationship Management", "Enterprise Resource Planning", "Supply Chain Optimization",
    "Quality Assurance Framework", "Performance Monitoring System", "Backup & Recovery Solution",
    "Disaster Recovery Planning", "Network Infrastructure Upgrade", "Database Optimization Project",
    "User Experience Enhancement", "Accessibility Compliance Initiative", "GDPR Compliance Program",
    "SOX Compliance Implementation", "Audit Management System", "Risk Assessment Platform",
    "Vendor Management Portal", "Employee Self-Service Platform", "Learning Management System",
    "Performance Management Tool", "Recruitment Platform", "Benefits Administration System",
    "Expense Management Solution", "Time Tracking Application", "Project Portfolio Management",
    "Resource Capacity Planning", "Financial Reporting System", "Budget Management Tool",
    "Cost Optimization Initiative", "Revenue Recognition System", "Tax Management Platform",
    "Compliance Monitoring System", "Document Management Solution", "Workflow Automation Engine",
    "Business Intelligence Platform", "Predictive Analytics Tool", "Machine Learning Pipeline",
    "IoT Data Collection System", "Blockchain Implementation", "Cryptocurrency Integration",
    "Social Media Analytics", "Marketing Automation Platform", "Campaign Management System",
    "Lead Generation Platform", "Customer Segmentation Tool", "Personalization Engine",
    "Recommendation System", "Search Optimization Tool", "SEO Enhancement Project",
    "Email Marketing Platform", "SMS Notification System", "Push Notification Service",
    "Video Streaming Platform", "Content Delivery Network", "Image Processing Service",
    "File Storage Solution", "Backup Service Migration", "Archive Management System",
    "Log Management Platform", "Monitoring & Alerting System", "Health Check Framework",
    "Load Testing Initiative", "Performance Tuning Project", "Scalability Enhancement",
    "High Availability Setup", "Fault Tolerance Implementation", "Circuit Breaker Pattern",
    "Rate Limiting Service", "Authentication Service", "Authorization Framework",
    "Single Sign-On Implementation", "Multi-Factor Authentication", "Password Management Tool",
    "Certificate Management System", "Encryption Key Management", "Data Loss Prevention",
    "Intrusion Detection System", "Security Information Management", "Vulnerability Assessment",
    "Penetration Testing Program", "Security Awareness Training", "Incident Response Plan",
    "Business Continuity Planning", "Change Management Process", "Configuration Management",
    "Release Management Pipeline", "Deployment Automation", "Infrastructure as Code",
    "Container Orchestration", "Serverless Architecture", "Edge Computing Implementation",
    "Progressive Web Application", "Native Mobile Development", "Cross-Platform Framework",
    "Responsive Web Design", "Accessibility Testing Tool", "Internationalization Support"
]

COMPANY_NAMES = [
    "TechCorp", "InnovateLabs", "DataSystems", "CloudFirst", "AgileWorks", "SmartSolutions",
    "NextGen", "ProActive", "Synergy", "Velocity", "Catalyst", "Pioneer", "Quantum",
    "Digital", "Fusion", "Matrix", "Nexus", "Vertex", "Apex", "Prime"
]

DESCRIPTIONS = [
    "Strategic initiative to enhance operational efficiency and customer experience",
    "Critical infrastructure upgrade to support business growth and scalability",
    "Innovation project focused on emerging technologies and market opportunities",
    "Compliance-driven initiative to meet regulatory requirements and standards",
    "Cost optimization program to improve margins and resource utilization",
    "Customer-centric project to improve satisfaction and engagement metrics",
    "Digital transformation effort to modernize legacy systems and processes",
    "Security enhancement program to protect against evolving cyber threats",
    "Performance improvement initiative to optimize system reliability and speed",
    "Integration project to streamline operations and improve data consistency"
]

async def create_sample_tenant():
    """Create a sample tenant"""
    tenant = {
        "_id": TENANT_ID,
        "name": "Sample Enterprise Corp",
        "code": "SAMPLE",
        "domain": "sample-enterprise.com",
        "subscription_tier": "enterprise",
        "status": "active",
        "settings": {
            "max_users": 1000,
            "max_projects": 500,
            "features": ["portfolios", "gantt", "reports", "integrations"]
        },
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "is_active": True
    }
    return tenant

async def create_sample_users():
    """Create sample users with different roles"""
    users = []
    
    # Admin user
    users.append({
        "_id": str(uuid.uuid4()),
        "tenant_id": TENANT_ID,
        "username": "admin",
        "email": "admin@sample-enterprise.com",
        "full_name": "System Administrator",
        "hashed_password": get_password_hash("password123"),
        "role": "admin",
        "status": "active",
        "job_title": "System Administrator",
        "department": "IT",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "is_active": True
    })

    # PMO Admin
    users.append({
        "_id": str(uuid.uuid4()),
        "tenant_id": TENANT_ID,
        "username": "pmo_admin",
        "email": "pmo@sample-enterprise.com",
        "full_name": "PMO Administrator",
        "hashed_password": get_password_hash("password123"),
        "role": "pmo_admin",
        "status": "active",
        "job_title": "PMO Director",
        "department": "PMO",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "is_active": True
    })

    # Portfolio Managers
    for i in range(5):
        users.append({
            "_id": str(uuid.uuid4()),
            "tenant_id": TENANT_ID,
            "username": f"portfolio_mgr_{i+1}",
            "email": f"portfolio.mgr{i+1}@sample-enterprise.com",
            "full_name": f"Portfolio Manager {i+1}",
            "hashed_password": get_password_hash("password123"),
            "role": "portfolio_manager",
            "status": "active",
            "job_title": "Portfolio Manager",
            "department": "PMO",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_active": True
        })

    # Project Managers
    for i in range(20):
        users.append({
            "_id": str(uuid.uuid4()),
            "tenant_id": TENANT_ID,
            "username": f"project_mgr_{i+1}",
            "email": f"pm{i+1}@sample-enterprise.com",
            "full_name": f"Project Manager {i+1}",
            "hashed_password": get_password_hash("password123"),
            "role": "project_manager",
            "status": "active",
            "job_title": "Project Manager",
            "department": random.choice(["Engineering", "Marketing", "Operations", "Finance"]),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_active": True
        })

    # Resources
    for i in range(50):
        users.append({
            "_id": str(uuid.uuid4()),
            "tenant_id": TENANT_ID,
            "username": f"developer_{i+1}",
            "email": f"dev{i+1}@sample-enterprise.com",
            "full_name": f"Developer {i+1}",
            "hashed_password": get_password_hash("password123"),
            "role": "resource",
            "status": "active",
            "job_title": random.choice(["Senior Developer", "Developer", "Junior Developer", "Analyst", "Designer"]),
            "department": random.choice(["Engineering", "Design", "QA", "DevOps"]),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_active": True
        })

    return users

async def create_strategic_objectives():
    """Create sample strategic objectives"""
    objectives = []
    
    obj_names = [
        "Increase Revenue Growth", "Improve Customer Satisfaction", "Enhance Operational Efficiency",
        "Digital Transformation", "Market Expansion", "Cost Optimization", "Innovation Leadership",
        "Regulatory Compliance", "Talent Development", "Sustainability Initiatives"
    ]
    
    for i, name in enumerate(obj_names):
        objectives.append({
            "_id": str(uuid.uuid4()),
            "tenant_id": TENANT_ID,
            "name": name,
            "code": f"OBJ-{i+1:03d}",
            "description": f"Strategic objective focused on {name.lower()}",
            "objective_type": random.choice(["financial", "customer", "internal_process", "learning_growth"]),
            "status": "active",
            "priority": random.choice(PRIORITIES),
            "owner_id": SAMPLE_USERS[2]["_id"],  # Portfolio manager
            "stakeholders": [SAMPLE_USERS[1]["_id"]],  # PMO admin
            "start_date": date.today().isoformat(),
            "target_date": (date.today() + timedelta(days=365)).isoformat(),
            "kpis": [],
            "success_criteria": [f"Achieve target metrics for {name.lower()}"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_active": True
        })
    
    return objectives

async def create_sample_portfolios():
    """Create sample portfolios"""
    portfolios = []
    
    portfolio_names = [
        "Digital Transformation Initiative", "Customer Experience Enhancement", 
        "Operational Excellence Program", "Innovation Lab Projects",
        "Infrastructure Modernization", "Compliance & Security Framework",
        "Market Expansion Strategy", "Product Development Pipeline",
        "Cost Optimization Initiative", "Sustainability Program"
    ]
    
    for i, name in enumerate(portfolio_names):
        portfolio = {
            "_id": str(uuid.uuid4()),
            "tenant_id": TENANT_ID,
            "name": name,
            "code": f"PF-{i+1:03d}",
            "description": random.choice(DESCRIPTIONS),
            "portfolio_type": random.choice(["strategic", "operational", "innovation", "maintenance"]),
            "status": random.choice(["active", "active", "active", "draft"]),  # More active portfolios
            "health_status": random.choice(["green", "green", "yellow", "red"]),  # More green
            "priority": random.choice(PRIORITIES),
            "portfolio_manager_id": random.choice([u["_id"] for u in SAMPLE_USERS if u["role"] == "portfolio_manager"]),
            "sponsors": [SAMPLE_USERS[1]["_id"]],
            "stakeholders": [SAMPLE_USERS[0]["_id"], SAMPLE_USERS[1]["_id"]],
            "start_date": date.today() - timedelta(days=random.randint(30, 365)),
            "end_date": date.today() + timedelta(days=random.randint(180, 730)),
            "financial_metrics": {
                "total_budget": float(random.randint(500000, 5000000)),
                "allocated_budget": 0,  # Will be calculated
                "spent_amount": 0,      # Will be calculated
                "committed_amount": 0,  # Will be calculated
                "forecasted_cost": 0,
                "npv": float(random.randint(100000, 1000000)),
                "irr": random.uniform(0.1, 0.3),
                "roi_percentage": random.uniform(15, 45),
                "payback_period_months": random.randint(12, 36)
            },
            "risk_metrics": {
                "risk_score": random.uniform(0.1, 0.6),
                "high_risks_count": random.randint(0, 3),
                "medium_risks_count": random.randint(1, 5),
                "low_risks_count": random.randint(2, 8),
                "overdue_risks_count": random.randint(0, 2)
            },
            "kpis": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_active": True
        }
        portfolios.append(portfolio)
    
    return portfolios

async def create_sample_projects():
    """Create 100 sample projects"""
    projects = []
    
    project_managers = [u["_id"] for u in SAMPLE_USERS if u["role"] == "project_manager"]
    resources = [u["_id"] for u in SAMPLE_USERS if u["role"] == "resource"]
    
    for i in range(100):
        # Randomly assign to portfolio (70% chance)
        portfolio_id = random.choice(SAMPLE_PORTFOLIOS)["_id"] if random.random() < 0.7 else None
        
        start_date = date.today() - timedelta(days=random.randint(0, 180))
        duration = random.randint(30, 365)
        end_date = start_date + timedelta(days=duration)
        
        project = {
            "_id": str(uuid.uuid4()),
            "tenant_id": TENANT_ID,
            "name": f"{random.choice(PROJECT_NAMES)} {random.choice(COMPANY_NAMES)}",
            "code": f"PRJ-{i+1:03d}",
            "description": random.choice(DESCRIPTIONS),
            "project_type": random.choice(PROJECT_TYPES),
            "methodology": random.choice(PROJECT_METHODOLOGIES),
            "status": random.choice(["active", "active", "active", "draft", "on_hold", "completed"]),
            "health_status": random.choice(["green", "green", "yellow", "red"]),
            "priority": random.choice(PRIORITIES),
            "current_phase": random.choice(["initiation", "planning", "execution", "monitoring"]),
            "portfolio_id": portfolio_id,
            "project_manager_id": random.choice(project_managers),
            "sponsor_id": random.choice([u["_id"] for u in SAMPLE_USERS if u["role"] in ["portfolio_manager", "pmo_admin"]]),
            "team_members": random.sample(resources, random.randint(3, 10)),
            "planned_start_date": start_date.isoformat(),
            "planned_end_date": end_date.isoformat(),
            "actual_start_date": start_date.isoformat() if random.random() < 0.8 else None,
            "actual_end_date": None,
            "percent_complete": random.uniform(0, 95),
            "financials": {
                "total_budget": float(random.randint(50000, 500000)),
                "allocated_budget": float(random.randint(45000, 450000)),
                "spent_amount": float(random.randint(20000, 300000)),
                "committed_amount": float(random.randint(10000, 100000)),
                "forecasted_cost": float(random.randint(60000, 520000)),
                "budget_variance": float(random.randint(-50000, 50000)),
                "cost_to_complete": float(random.randint(10000, 200000)),
                "labor_cost": float(random.randint(30000, 300000)),
                "material_cost": float(random.randint(5000, 50000)),
                "vendor_cost": float(random.randint(10000, 100000)),
                "overhead_cost": float(random.randint(5000, 50000))
            },
            "risk_score": random.uniform(0.1, 0.8),
            "open_issues_count": random.randint(0, 5),
            "open_risks_count": random.randint(0, 3),
            "tasks": [],  # Will add tasks separately
            "milestones": [],  # Will add milestones separately
            "risks": [],
            "issues": [],
            "dependencies": [],
            "approvals": [],
            "baselines": [],
            "document_urls": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_active": True
        }
        
        # Add sample tasks
        task_count = random.randint(5, 15)
        for j in range(task_count):
            task = {
                "id": str(uuid.uuid4()),
                "name": f"Task {j+1}: {random.choice(['Design', 'Development', 'Testing', 'Documentation', 'Review'])} {random.choice(['Phase', 'Component', 'Module', 'Feature'])}",
                "description": f"Detailed work item for {project['name']}",
                "status": random.choice(["not_started", "in_progress", "completed", "on_hold"]),
                "priority": random.choice(PRIORITIES),
                "assignee_id": random.choice(project["team_members"]) if project["team_members"] else None,
                "planned_start_date": (start_date + timedelta(days=random.randint(0, 30))).isoformat(),
                "planned_end_date": (start_date + timedelta(days=random.randint(31, 60))).isoformat(),
                "estimated_hours": random.randint(8, 80),
                "actual_hours": random.randint(5, 85) if random.random() < 0.6 else None,
                "percent_complete": random.uniform(0, 100),
                "parent_task_id": None,
                "subtasks": [],
                "dependencies": [],
                "labels": random.sample(["frontend", "backend", "database", "api", "ui", "testing"], random.randint(1, 3)),
                "tags": [],
                "story_points": random.choice([1, 2, 3, 5, 8, 13]) if project["methodology"] in ["agile", "scrum"] else None
            }
            project["tasks"].append(task)
        
        # Add sample milestones
        milestone_count = random.randint(3, 8)
        for j in range(milestone_count):
            milestone_date = start_date + timedelta(days=random.randint(30, duration-30))
            milestone = {
                "id": str(uuid.uuid4()),
                "name": f"Milestone {j+1}: {random.choice(['Design Complete', 'Development Complete', 'Testing Complete', 'Go-Live', 'Phase Gate'])}",
                "description": f"Key milestone for {project['name']}",
                "planned_date": milestone_date.isoformat(),
                "actual_date": milestone_date.isoformat() if random.random() < 0.5 else None,
                "status": random.choice(["planned", "in_progress", "completed", "delayed"]),
                "deliverables": [f"Deliverable {k+1}" for k in range(random.randint(1, 3))],
                "dependencies": []
            }
            project["milestones"].append(milestone)
        
        # Add sample risks
        risk_count = random.randint(0, 5)
        for j in range(risk_count):
            risk = {
                "id": str(uuid.uuid4()),
                "title": f"Risk {j+1}: {random.choice(['Technical', 'Resource', 'Schedule', 'Budget', 'Quality'])} Risk",
                "description": f"Potential risk that could impact {project['name']}",
                "risk_level": random.choice(["low", "medium", "high"]),
                "probability": random.uniform(0.1, 0.8),
                "impact": random.uniform(0.2, 0.9),
                "owner_id": project["project_manager_id"],
                "identified_by": random.choice(project["team_members"]) if project["team_members"] else project["project_manager_id"],
                "identified_date": (start_date + timedelta(days=random.randint(0, 60))).isoformat(),
                "status": random.choice(["active", "active", "completed"]),
                "mitigation_plan": f"Mitigation strategy for risk in {project['name']}",
                "affected_tasks": [],
                "affected_milestones": []
            }
            project["risks"].append(risk)
        
        projects.append(project)
    
    return projects

async def create_portfolio_projects():
    """Create portfolio-project relationships"""
    relationships = []
    
    for project in SAMPLE_PROJECTS:
        if project.get("portfolio_id"):
            relationship = {
                "_id": str(uuid.uuid4()),
                "tenant_id": TENANT_ID,
                "portfolio_id": project["portfolio_id"],
                "project_id": project["_id"],
                "added_date": date.today() - timedelta(days=random.randint(0, 90)),
                "strategic_weight": random.uniform(0.1, 1.0),
                "budget_allocation": project["financials"]["total_budget"],
                "priority_ranking": random.randint(1, 10),
                "alignment_scores": {},
                "is_active": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            relationships.append(relationship)
    
    return relationships

async def main():
    """Main function to seed all sample data"""
    print("🌱 Starting AtlasPM sample data seeding...")
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(settings.MONGO_URL)
    db = client.atlaspm
    
    try:
        # Clear existing data (optional - comment out to preserve existing data)
        print("🗑️  Clearing existing sample data...")
        await db.tenants.delete_many({"_id": TENANT_ID})
        await db.users.delete_many({"tenant_id": TENANT_ID})
        await db.strategic_objectives.delete_many({"tenant_id": TENANT_ID})
        await db.portfolios.delete_many({"tenant_id": TENANT_ID})
        await db.projects.delete_many({"tenant_id": TENANT_ID})
        await db.portfolio_projects.delete_many({"tenant_id": TENANT_ID})
        
        # Create tenant
        print("🏢 Creating sample tenant...")
        tenant = await create_sample_tenant()
        await db.tenants.insert_one(tenant)
        
        # Create users
        print("👥 Creating sample users...")
        global SAMPLE_USERS
        SAMPLE_USERS = await create_sample_users()
        await db.users.insert_many(SAMPLE_USERS)
        print(f"   ✅ Created {len(SAMPLE_USERS)} users")
        
        # Create strategic objectives
        print("🎯 Creating strategic objectives...")
        objectives = await create_strategic_objectives()
        await db.strategic_objectives.insert_many(objectives)
        print(f"   ✅ Created {len(objectives)} strategic objectives")
        
        # Create portfolios
        print("📁 Creating sample portfolios...")
        global SAMPLE_PORTFOLIOS
        SAMPLE_PORTFOLIOS = await create_sample_portfolios()
        await db.portfolios.insert_many(SAMPLE_PORTFOLIOS)
        print(f"   ✅ Created {len(SAMPLE_PORTFOLIOS)} portfolios")
        
        # Create projects
        print("🚀 Creating 100 sample projects...")
        global SAMPLE_PROJECTS
        SAMPLE_PROJECTS = await create_sample_projects()
        await db.projects.insert_many(SAMPLE_PROJECTS)
        print(f"   ✅ Created {len(SAMPLE_PROJECTS)} projects")
        
        # Create portfolio-project relationships
        print("🔗 Creating portfolio-project relationships...")
        relationships = await create_portfolio_projects()
        if relationships:
            await db.portfolio_projects.insert_many(relationships)
            print(f"   ✅ Created {len(relationships)} portfolio-project relationships")
        
        # Update portfolio financial metrics
        print("💰 Updating portfolio financial metrics...")
        for portfolio in SAMPLE_PORTFOLIOS:
            # Get projects in this portfolio
            portfolio_projects = [p for p in SAMPLE_PROJECTS if p.get("portfolio_id") == portfolio["_id"]]
            
            if portfolio_projects:
                allocated_budget = sum(p["financials"]["total_budget"] for p in portfolio_projects)
                spent_amount = sum(p["financials"]["spent_amount"] for p in portfolio_projects)
                committed_amount = sum(p["financials"]["committed_amount"] for p in portfolio_projects)
                
                await db.portfolios.update_one(
                    {"_id": portfolio["_id"]},
                    {"$set": {
                        "financial_metrics.allocated_budget": allocated_budget,
                        "financial_metrics.spent_amount": spent_amount,
                        "financial_metrics.committed_amount": committed_amount,
                        "updated_at": datetime.utcnow()
                    }}
                )
        
        print("\n🎉 Sample data seeding completed successfully!")
        print("\n📊 Summary:")
        print(f"   • 1 Tenant: {TENANT_ID}")
        print(f"   • {len(SAMPLE_USERS)} Users (1 admin, 1 PMO admin, 5 portfolio managers, 20 project managers, 50 resources)")
        print(f"   • {len(objectives)} Strategic Objectives")
        print(f"   • {len(SAMPLE_PORTFOLIOS)} Portfolios")
        print(f"   • {len(SAMPLE_PROJECTS)} Projects")
        print(f"   • {len(relationships)} Portfolio-Project relationships")
        
        print("\n🔐 Sample Login Credentials:")
        print("   • Admin: username='admin', password='password123'")
        print("   • PMO Admin: username='pmo_admin', password='password123'")
        print("   • Portfolio Manager: username='portfolio_mgr_1', password='password123'")
        print("   • Project Manager: username='project_mgr_1', password='password123'")
        print("   • Developer: username='developer_1', password='password123'")
        
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main())
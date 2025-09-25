#!/usr/bin/env python3
"""
AtlasPM Demo Data Creation Script

This script creates demo tenants, users, portfolios, and projects for testing.
"""

import asyncio
import uuid
from datetime import datetime, date, timedelta
from pymongo import MongoClient
import hashlib
from motor.motor_asyncio import AsyncIOMotorClient

def hash_password(password: str) -> str:
    """Simple password hashing for demo purposes"""
    return hashlib.sha256(password.encode()).hexdigest()

# MongoDB connection
MONGO_URL = "mongodb://localhost:27017/atlaspm"

async def create_demo_data():
    """Create comprehensive demo data for AtlasPM"""
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGO_URL)
    db = client.get_default_database()
    
    print("🚀 Creating AtlasPM Demo Data...")
    
    # Clear existing data
    collections = ['tenants', 'users', 'portfolios', 'projects', 'audit_logs']
    for collection in collections:
        await db[collection].delete_many({})
    print("✅ Cleared existing data")
    
    # Demo data structure
    demo_data = {
        # Demo Tenant 1: TechCorp
        "techcorp": {
            "tenant": {
                "name": "TechCorp Industries", 
                "code": "techcorp",
                "domain": "techcorp.com",
                "admin_name": "John Admin",
                "admin_email": "admin@techcorp.com"
            },
            "users": [
                {"username": "admin_techcorp", "email": "admin@techcorp.com", "full_name": "John Admin", "role": "admin", "password": "Demo123!"},
                {"username": "pm_sarah", "email": "sarah.pm@techcorp.com", "full_name": "Sarah Johnson", "role": "portfolio_manager", "password": "Demo123!"},
                {"username": "mgr_mike", "email": "mike.mgr@techcorp.com", "full_name": "Mike Davis", "role": "project_manager", "password": "Demo123!"},
                {"username": "dev_alice", "email": "alice.dev@techcorp.com", "full_name": "Alice Cooper", "role": "resource", "password": "Demo123!"},
                {"username": "finance_bob", "email": "bob.finance@techcorp.com", "full_name": "Bob Wilson", "role": "finance", "password": "Demo123!"},
            ]
        },
        
        # Demo Tenant 2: StartupXYZ  
        "startupxyz": {
            "tenant": {
                "name": "StartupXYZ",
                "code": "startupxyz", 
                "domain": "startupxyz.io",
                "admin_name": "Jane Founder",
                "admin_email": "jane@startupxyz.io"
            },
            "users": [
                {"username": "admin_startup", "email": "jane@startupxyz.io", "full_name": "Jane Founder", "role": "admin", "password": "Demo123!"},
                {"username": "cto_alex", "email": "alex.cto@startupxyz.io", "full_name": "Alex Thompson", "role": "pmo_admin", "password": "Demo123!"},
                {"username": "lead_emma", "email": "emma.lead@startupxyz.io", "full_name": "Emma Rodriguez", "role": "project_manager", "password": "Demo123!"},
                {"username": "dev_david", "email": "david.dev@startupxyz.io", "full_name": "David Kim", "role": "resource", "password": "Demo123!"},
            ]
        },
        
        # Demo Tenant 3: Enterprise Solutions
        "enterprise": {
            "tenant": {
                "name": "Enterprise Solutions Ltd",
                "code": "enterprise",
                "domain": "enterprise-sol.com", 
                "admin_name": "Robert Enterprise",
                "admin_email": "robert@enterprise-sol.com"
            },
            "users": [
                {"username": "admin_ent", "email": "robert@enterprise-sol.com", "full_name": "Robert Enterprise", "role": "admin", "password": "Demo123!"},
                {"username": "pmo_lisa", "email": "lisa.pmo@enterprise-sol.com", "full_name": "Lisa Chang", "role": "pmo_admin", "password": "Demo123!"},
                {"username": "pm_carlos", "email": "carlos.pm@enterprise-sol.com", "full_name": "Carlos Martinez", "role": "project_manager", "password": "Demo123!"},
                {"username": "analyst_mary", "email": "mary.analyst@enterprise-sol.com", "full_name": "Mary Johnson", "role": "viewer", "password": "Demo123!"},
            ]
        }
    }
    
    # Create tenants and users
    tenant_ids = {}
    user_ids = {}
    
    for tenant_key, tenant_data in demo_data.items():
        # Create tenant
        tenant_id = str(uuid.uuid4())
        tenant_ids[tenant_key] = tenant_id
        
        tenant_doc = {
            "_id": tenant_id,
            "name": tenant_data["tenant"]["name"],
            "code": tenant_data["tenant"]["code"],
            "domain": tenant_data["tenant"]["domain"],
            "status": "active",
            "plan": "professional",
            "admin_email": tenant_data["tenant"]["admin_email"],
            "admin_name": tenant_data["tenant"]["admin_name"],
            "max_users": 100,
            "max_projects": 500,
            "settings": {
                "date_format": "MM/DD/YYYY",
                "time_zone": "UTC",
                "currency": "USD",
                "language": "en"
            },
            "sso_enabled": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        await db.tenants.insert_one(tenant_doc)
        print(f"✅ Created tenant: {tenant_data['tenant']['name']} ({tenant_data['tenant']['code']})")
        
        # Create users for this tenant
        tenant_user_ids = {}
        for user_data in tenant_data["users"]:
            user_id = str(uuid.uuid4())
            tenant_user_ids[user_data["username"]] = user_id
            
            user_doc = {
                "_id": user_id,
                "tenant_id": tenant_id,
                "username": user_data["username"],
                "email": user_data["email"],
                "full_name": user_data["full_name"],
                "hashed_password": hash_password(user_data["password"]),
                "role": user_data["role"],
                "status": "active",
                "job_title": f"{user_data['role'].replace('_', ' ').title()}",
                "department": "Demo Department",
                "permissions": [],
                "portfolio_access": [],
                "project_access": [],
                "failed_login_attempts": 0,
                "preferences": {},
                "is_active": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "created_by": user_id
            }
            
            await db.users.insert_one(user_doc)
            print(f"   ✅ Created user: {user_data['full_name']} ({user_data['username']}) - {user_data['role']}")
        
        user_ids[tenant_key] = tenant_user_ids
    
    # Create sample portfolios and projects
    portfolio_data = {
        "techcorp": [
            {
                "name": "Digital Transformation Initiative",
                "code": "DTI-2024",
                "description": "Modernizing legacy systems and implementing cloud-first architecture",
                "portfolio_type": "strategic",
                "priority": "high",
                "projects": [
                    {"name": "Cloud Migration Phase 1", "code": "CM-001", "type": "infrastructure"},
                    {"name": "Customer Portal Redesign", "code": "CPR-002", "type": "software_development"},
                    {"name": "Data Analytics Platform", "code": "DAP-003", "type": "software_development"}
                ]
            },
            {
                "name": "Product Innovation Hub", 
                "code": "PIH-2024",
                "description": "Next-generation product development and R&D initiatives",
                "portfolio_type": "innovation",
                "priority": "medium",
                "projects": [
                    {"name": "AI-Powered Features", "code": "AI-001", "type": "research"},
                    {"name": "Mobile App v2.0", "code": "MOB-002", "type": "software_development"}
                ]
            }
        ],
        "startupxyz": [
            {
                "name": "MVP Development",
                "code": "MVP-2024", 
                "description": "Building and launching our minimum viable product",
                "portfolio_type": "strategic",
                "priority": "critical",
                "projects": [
                    {"name": "Core Platform Development", "code": "CORE-001", "type": "software_development"},
                    {"name": "User Authentication System", "code": "AUTH-002", "type": "software_development"},
                    {"name": "Payment Integration", "code": "PAY-003", "type": "software_development"}
                ]
            }
        ],
        "enterprise": [
            {
                "name": "Enterprise Compliance Program",
                "code": "ECP-2024",
                "description": "Ensuring regulatory compliance across all business units", 
                "portfolio_type": "operational",
                "priority": "high",
                "projects": [
                    {"name": "GDPR Compliance Audit", "code": "GDPR-001", "type": "compliance"},
                    {"name": "Security Framework Update", "code": "SEC-002", "type": "compliance"},
                    {"name": "Staff Training Program", "code": "TRAIN-003", "type": "process_improvement"}
                ]
            }
        ]
    }
    
    for tenant_key, portfolios in portfolio_data.items():
        tenant_id = tenant_ids[tenant_key]
        
        # Get portfolio manager (first PM or admin)
        pm_users = [uid for username, uid in user_ids[tenant_key].items() 
                   if 'pm' in username or 'admin' in username]
        portfolio_manager_id = pm_users[0] if pm_users else list(user_ids[tenant_key].values())[0]
        
        for portfolio_info in portfolios:
            portfolio_id = str(uuid.uuid4())
            
            portfolio_doc = {
                "_id": portfolio_id,
                "tenant_id": tenant_id,
                "name": portfolio_info["name"],
                "code": portfolio_info["code"],
                "description": portfolio_info["description"],
                "portfolio_type": portfolio_info["portfolio_type"],
                "status": "active",
                "health_status": "green",
                "priority": portfolio_info["priority"],
                "portfolio_manager_id": portfolio_manager_id,
                "sponsors": [portfolio_manager_id],
                "stakeholders": list(user_ids[tenant_key].values())[:3],
                "strategic_objectives": [],
                "start_date": date.today(),
                "end_date": date.today() + timedelta(days=365),
                "financial_metrics": {
                    "total_budget": 500000.00,
                    "allocated_budget": 300000.00,
                    "spent_amount": 150000.00
                },
                "risk_metrics": {
                    "risk_score": 0.3,
                    "high_risks_count": 1,
                    "medium_risks_count": 3,
                    "low_risks_count": 5
                },
                "project_ids": [],
                "settings": {},
                "is_active": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "created_by": portfolio_manager_id,
                "updated_by": portfolio_manager_id
            }
            
            await db.portfolios.insert_one(portfolio_doc)
            print(f"   ✅ Created portfolio: {portfolio_info['name']} ({portfolio_info['code']})")
            
            # Create projects for this portfolio
            project_ids = []
            for project_info in portfolio_info["projects"]:
                project_id = str(uuid.uuid4())
                project_ids.append(project_id)
                
                # Get project manager
                project_manager_id = portfolio_manager_id
                if 'mgr' in user_ids[tenant_key]:
                    project_manager_id = [uid for username, uid in user_ids[tenant_key].items() 
                                        if 'mgr' in username][0]
                
                project_doc = {
                    "_id": project_id,
                    "tenant_id": tenant_id,
                    "portfolio_id": portfolio_id,
                    "name": project_info["name"],
                    "code": project_info["code"],
                    "description": f"Project for {project_info['name']} - part of {portfolio_info['name']}",
                    "project_type": project_info["type"],
                    "methodology": "agile",
                    "status": "active",
                    "health_status": "green", 
                    "priority": "medium",
                    "project_manager_id": project_manager_id,
                    "sponsor_id": portfolio_manager_id,
                    "team_members": list(user_ids[tenant_key].values())[:4],
                    "planned_start_date": date.today(),
                    "planned_end_date": date.today() + timedelta(days=90),
                    "percent_complete": 35.5,
                    "milestones": [
                        {
                            "id": str(uuid.uuid4()),
                            "name": "Project Kickoff",
                            "planned_date": date.today() + timedelta(days=7),
                            "status": "completed"
                        },
                        {
                            "id": str(uuid.uuid4()),
                            "name": "Phase 1 Completion", 
                            "planned_date": date.today() + timedelta(days=30),
                            "status": "in_progress"
                        },
                        {
                            "id": str(uuid.uuid4()),
                            "name": "Final Delivery",
                            "planned_date": date.today() + timedelta(days=90),
                            "status": "planned"
                        }
                    ],
                    "financials": {
                        "total_budget": 100000.00,
                        "allocated_budget": 80000.00,
                        "spent_amount": 25000.00,
                        "labor_cost": 20000.00,
                        "material_cost": 3000.00,
                        "vendor_cost": 2000.00
                    },
                    "resource_allocations": [],
                    "risk_score": 0.2,
                    "open_issues_count": 2,
                    "open_risks_count": 1,
                    "document_urls": [],
                    "custom_fields": {},
                    "is_active": True,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow(),
                    "created_by": project_manager_id,
                    "updated_by": project_manager_id
                }
                
                await db.projects.insert_one(project_doc)
                print(f"      ✅ Created project: {project_info['name']} ({project_info['code']})")
            
            # Update portfolio with project IDs
            await db.portfolios.update_one(
                {"_id": portfolio_id},
                {"$set": {"project_ids": project_ids}}
            )
    
    print("\n🎉 Demo data creation completed successfully!")
    print("\n📋 DEMO LOGIN CREDENTIALS:")
    print("=" * 50)
    
    for tenant_key, tenant_data in demo_data.items():
        tenant_info = tenant_data["tenant"]
        print(f"\n🏢 {tenant_info['name']} ({tenant_info['code']})")
        print("-" * 40)
        
        for user in tenant_data["users"]:
            print(f"👤 {user['full_name']} ({user['role']})")
            print(f"   Username: {user['username']}")
            print(f"   Password: {user['password']}")
            print(f"   Tenant Code: {tenant_info['code']}")
            print()
    
    print("🌐 Access the application at: http://localhost:3000")
    print("🔗 API Documentation: http://localhost:8001/docs")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_demo_data())
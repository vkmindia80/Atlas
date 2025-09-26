#!/usr/bin/env python3
"""
Simple API test script to verify the enhanced portfolio and project endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8001/api/v1"

def login():
    """Login and get access token"""
    login_data = {
        "username": "admin",
        "password": "password123",
        "tenant_code": "SAMPLE"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Login failed: {response.status_code} - {response.text}")
        return None

def get_headers(token):
    """Get authorization headers"""
    return {"Authorization": f"Bearer {token}"}

def test_portfolios(token):
    """Test portfolio endpoints"""
    headers = get_headers(token)
    
    print("\n🗂️  Testing Portfolio Endpoints")
    print("=" * 50)
    
    # Test get portfolios
    response = requests.get(f"{BASE_URL}/portfolios/", headers=headers)
    print(f"GET /portfolios/: {response.status_code}")
    
    if response.status_code == 200:
        portfolios = response.json()
        print(f"  Found {len(portfolios)} portfolios")
        
        if portfolios:
            portfolio_id = portfolios[0]["id"]
            print(f"  Testing with portfolio ID: {portfolio_id}")
            
            # Test get portfolio detail
            response = requests.get(f"{BASE_URL}/portfolios/{portfolio_id}", headers=headers)
            print(f"GET /portfolios/{portfolio_id}: {response.status_code}")
            
            # Test portfolio dashboard
            response = requests.get(f"{BASE_URL}/portfolios/{portfolio_id}/dashboard", headers=headers)
            print(f"GET /portfolios/{portfolio_id}/dashboard: {response.status_code}")
            if response.status_code == 200:
                dashboard = response.json()
                print(f"  Dashboard KPIs: {list(dashboard.get('kpis', {}).keys())}")
    
    # Test strategic objectives
    response = requests.get(f"{BASE_URL}/portfolios/objectives/", headers=headers)
    print(f"GET /portfolios/objectives/: {response.status_code}")

def test_projects(token):
    """Test project endpoints"""
    headers = get_headers(token)
    
    print("\n🚀 Testing Project Endpoints")
    print("=" * 50)
    
    # Test get projects
    response = requests.get(f"{BASE_URL}/projects/", headers=headers)
    print(f"GET /projects/: {response.status_code}")
    
    if response.status_code == 200:
        projects = response.json()
        print(f"  Found {len(projects)} projects")
        
        if projects:
            project_id = projects[0]["id"]
            print(f"  Testing with project ID: {project_id}")
            
            # Test get project detail
            response = requests.get(f"{BASE_URL}/projects/{project_id}", headers=headers)
            print(f"GET /projects/{project_id}: {response.status_code}")
            if response.status_code == 200:
                detail = response.json()
                print(f"  Project has {detail.get('task_summary', {}).get('total', 0)} tasks")

def main():
    print("🧪 AtlasPM API Testing")
    print("=" * 50)
    
    # Login
    print("🔐 Logging in...")
    token = login()
    
    if not token:
        print("❌ Failed to login")
        return
    
    print("✅ Login successful")
    
    # Test endpoints
    try:
        test_portfolios(token)
        test_projects(token)
        print("\n🎉 API testing completed!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    main()
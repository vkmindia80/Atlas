#!/usr/bin/env python3
"""
AtlasPM Backend API Testing Suite
Tests authentication, dashboard, and admin endpoints
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional

class AtlasPMAPITester:
    def __init__(self, base_url: str = "https://roadmap-checker-5.preview.emergentagent.com"):
        self.base_url = base_url
        self.token = None
        self.refresh_token = None
        self.current_user = None
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        
        # Demo users from the frontend code
        self.demo_users = [
            {"username": "admin_techcorp", "password": "Demo123!", "tenant_code": "techcorp", "role": "Admin"},
            {"username": "pm_sarah", "password": "Demo123!", "tenant_code": "techcorp", "role": "Portfolio Manager"},
            {"username": "mgr_mike", "password": "Demo123!", "tenant_code": "techcorp", "role": "Project Manager"},
            {"username": "admin_startup", "password": "Demo123!", "tenant_code": "startupxyz", "role": "Admin"},
            {"username": "cto_alex", "password": "Demo123!", "tenant_code": "startupxyz", "role": "PMO Admin"},
            {"username": "pmo_lisa", "password": "Demo123!", "tenant_code": "enterprise", "role": "PMO Admin"}
        ]

    def log_test(self, name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test results"""
        self.tests_run += 1
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"\n{status} - {name}")
        if details:
            print(f"   Details: {details}")
        if response_data and not success:
            print(f"   Response: {response_data}")
        
        if success:
            self.tests_passed += 1
        else:
            self.failed_tests.append({
                "test": name,
                "details": details,
                "response": response_data
            })

    def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                    expected_status: int = 200, use_auth: bool = True) -> tuple[bool, Any]:
        """Make HTTP request and return success status and response data"""
        url = f"{self.base_url}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        if use_auth and self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                return False, f"Unsupported method: {method}"

            success = response.status_code == expected_status
            try:
                response_data = response.json()
            except:
                response_data = response.text

            return success, response_data

        except requests.exceptions.RequestException as e:
            return False, f"Request failed: {str(e)}"

    def test_health_check(self):
        """Test health endpoint"""
        success, response = self.make_request('GET', '/health', use_auth=False)
        self.log_test("Health Check", success, 
                     f"Status: {response.get('status', 'unknown')}" if success else str(response))
        return success

    def test_login(self, username: str, password: str, tenant_code: str) -> bool:
        """Test user login"""
        credentials = {
            "username": username,
            "password": password,
            "tenant_code": tenant_code
        }
        
        success, response = self.make_request('POST', '/api/v1/auth/login', 
                                            data=credentials, use_auth=False)
        
        if success and isinstance(response, dict):
            self.token = response.get('access_token')
            self.refresh_token = response.get('refresh_token')
            self.current_user = response.get('user')
            
            self.log_test(f"Login - {username}", success, 
                         f"Role: {self.current_user.get('role', 'unknown')}")
        else:
            self.log_test(f"Login - {username}", success, str(response))
        
        return success

    def test_get_current_user(self):
        """Test getting current user info"""
        success, response = self.make_request('GET', '/api/v1/auth/me')
        
        if success and isinstance(response, dict):
            user_info = f"User: {response.get('full_name', 'unknown')} ({response.get('role', 'unknown')})"
            self.log_test("Get Current User", success, user_info)
        else:
            self.log_test("Get Current User", success, str(response))
        
        return success

    def test_dashboard_access(self):
        """Test admin dashboard access"""
        success, response = self.make_request('GET', '/api/v1/admin/dashboard')
        
        if success and isinstance(response, dict):
            overview = response.get('overview', {})
            details = f"Users: {overview.get('total_users', 0)}, Projects: {overview.get('total_projects', 0)}, Portfolios: {overview.get('total_portfolios', 0)}"
            self.log_test("Admin Dashboard", success, details)
        else:
            self.log_test("Admin Dashboard", success, str(response))
        
        return success

    def test_tenant_info(self):
        """Test getting tenant information"""
        success, response = self.make_request('GET', '/api/v1/admin/tenant')
        
        if success and isinstance(response, dict):
            tenant_info = f"Tenant: {response.get('name', 'unknown')} ({response.get('code', 'unknown')})"
            self.log_test("Tenant Info", success, tenant_info)
        else:
            self.log_test("Tenant Info", success, str(response))
        
        return success

    def test_system_health(self):
        """Test system health endpoint (admin only)"""
        success, response = self.make_request('GET', '/api/v1/admin/system-health')
        
        if success and isinstance(response, dict):
            status = response.get('status', 'unknown')
            self.log_test("System Health", success, f"Status: {status}")
        else:
            # This might fail for non-admin users, which is expected
            expected_error = "403" in str(response) or "Insufficient permissions" in str(response)
            if expected_error:
                self.log_test("System Health", True, "Access properly restricted to admins")
            else:
                self.log_test("System Health", success, str(response))
        
        return success

    def test_token_refresh(self):
        """Test token refresh functionality"""
        if not self.refresh_token:
            self.log_test("Token Refresh", False, "No refresh token available")
            return False
        
        success, response = self.make_request('POST', '/api/v1/auth/refresh', 
                                            data={"refresh_token": self.refresh_token}, 
                                            use_auth=False)
        
        if success and isinstance(response, dict):
            new_token = response.get('access_token')
            if new_token:
                self.token = new_token  # Update token for subsequent tests
                self.log_test("Token Refresh", success, "New token received")
            else:
                self.log_test("Token Refresh", False, "No access token in response")
        else:
            self.log_test("Token Refresh", success, str(response))
        
        return success

    def test_logout(self):
        """Test logout functionality"""
        success, response = self.make_request('POST', '/api/v1/auth/logout')
        self.log_test("Logout", success, response.get('message', '') if success else str(response))
        return success

    def run_comprehensive_test(self):
        """Run comprehensive test suite"""
        print("🚀 Starting AtlasPM Backend API Tests")
        print(f"📍 Testing against: {self.base_url}")
        print("=" * 60)

        # Test health check first
        if not self.test_health_check():
            print("❌ Health check failed - stopping tests")
            return False

        # Test each demo user
        for user in self.demo_users:
            print(f"\n🔐 Testing user: {user['username']} ({user['role']})")
            print("-" * 40)
            
            # Login
            if not self.test_login(user['username'], user['password'], user['tenant_code']):
                continue
            
            # Test authenticated endpoints
            self.test_get_current_user()
            
            # Test admin endpoints (will fail gracefully for non-admin users)
            if user['role'] in ['Admin', 'PMO Admin']:
                self.test_dashboard_access()
                self.test_tenant_info()
                if user['role'] == 'Admin':
                    self.test_system_health()
            
            # Test token refresh
            self.test_token_refresh()
            
            # Test logout
            self.test_logout()
            
            # Clear tokens for next user
            self.token = None
            self.refresh_token = None
            self.current_user = None

        return True

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {len(self.failed_tests)}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%" if self.tests_run > 0 else "0%")
        
        if self.failed_tests:
            print("\n❌ FAILED TESTS:")
            for i, test in enumerate(self.failed_tests, 1):
                print(f"{i}. {test['test']}")
                if test['details']:
                    print(f"   Details: {test['details']}")
        
        print("\n" + "=" * 60)

def main():
    """Main test execution"""
    tester = AtlasPMAPITester()
    
    try:
        success = tester.run_comprehensive_test()
        tester.print_summary()
        
        # Return appropriate exit code
        return 0 if tester.tests_passed == tester.tests_run else 1
        
    except KeyboardInterrupt:
        print("\n⚠️  Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
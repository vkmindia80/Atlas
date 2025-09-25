<file>
      <absolute_file_name>/app/backend/app/utils/rbac.py</absolute_file_name>
      <content">from typing import List, Dict, Set
from enum import Enum
from ..models.user import UserRole

class Permission(str, Enum):
    # Tenant management
    MANAGE_TENANT = "manage_tenant"
    VIEW_TENANT = "view_tenant"
    
    # User management
    MANAGE_USERS = "manage_users"
    VIEW_USERS = "view_users"
    INVITE_USERS = "invite_users"
    
    # Portfolio management
    CREATE_PORTFOLIO = "create_portfolio"
    EDIT_PORTFOLIO = "edit_portfolio"
    DELETE_PORTFOLIO = "delete_portfolio"
    VIEW_PORTFOLIO = "view_portfolio"
    MANAGE_PORTFOLIO_MEMBERS = "manage_portfolio_members"
    
    # Project management
    CREATE_PROJECT = "create_project"
    EDIT_PROJECT = "edit_project"
    DELETE_PROJECT = "delete_project"
    VIEW_PROJECT = "view_project"
    MANAGE_PROJECT_MEMBERS = "manage_project_members"
    APPROVE_PROJECT_CHANGES = "approve_project_changes"
    
    # Resource management
    MANAGE_RESOURCES = "manage_resources"
    VIEW_RESOURCES = "view_resources"
    ASSIGN_RESOURCES = "assign_resources"
    VIEW_RESOURCE_UTILIZATION = "view_resource_utilization"
    
    # Financial management
    MANAGE_BUDGETS = "manage_budgets"
    VIEW_BUDGETS = "view_budgets"
    APPROVE_BUDGETS = "approve_budgets"
    VIEW_FINANCIAL_REPORTS = "view_financial_reports"
    
    # Time tracking
    ENTER_TIME = "enter_time"
    APPROVE_TIME = "approve_time"
    VIEW_TIME_REPORTS = "view_time_reports"
    
    # Risk management
    MANAGE_RISKS = "manage_risks"
    VIEW_RISKS = "view_risks"
    
    # Reporting
    VIEW_REPORTS = "view_reports"
    CREATE_REPORTS = "create_reports"
    EXPORT_DATA = "export_data"
    
    # System administration
    VIEW_AUDIT_LOGS = "view_audit_logs"
    MANAGE_INTEGRATIONS = "manage_integrations"

# Role-based permission mapping
ROLE_PERMISSIONS: Dict[UserRole, Set[Permission]] = {
    UserRole.ADMIN: {
        # Full platform administration
        Permission.MANAGE_TENANT,
        Permission.VIEW_TENANT,
        Permission.MANAGE_USERS,
        Permission.VIEW_USERS,
        Permission.INVITE_USERS,
        Permission.CREATE_PORTFOLIO,
        Permission.EDIT_PORTFOLIO,
        Permission.DELETE_PORTFOLIO,
        Permission.VIEW_PORTFOLIO,
        Permission.MANAGE_PORTFOLIO_MEMBERS,
        Permission.CREATE_PROJECT,
        Permission.EDIT_PROJECT,
        Permission.DELETE_PROJECT,
        Permission.VIEW_PROJECT,
        Permission.MANAGE_PROJECT_MEMBERS,
        Permission.APPROVE_PROJECT_CHANGES,
        Permission.MANAGE_RESOURCES,
        Permission.VIEW_RESOURCES,
        Permission.ASSIGN_RESOURCES,
        Permission.VIEW_RESOURCE_UTILIZATION,
        Permission.MANAGE_BUDGETS,
        Permission.VIEW_BUDGETS,
        Permission.APPROVE_BUDGETS,
        Permission.VIEW_FINANCIAL_REPORTS,
        Permission.APPROVE_TIME,
        Permission.VIEW_TIME_REPORTS,
        Permission.MANAGE_RISKS,
        Permission.VIEW_RISKS,
        Permission.VIEW_REPORTS,
        Permission.CREATE_REPORTS,
        Permission.EXPORT_DATA,
        Permission.VIEW_AUDIT_LOGS,
        Permission.MANAGE_INTEGRATIONS,
    },
    
    UserRole.PMO_ADMIN: {
        # PMO-level administration
        Permission.VIEW_TENANT,
        Permission.MANAGE_USERS,
        Permission.VIEW_USERS,
        Permission.INVITE_USERS,
        Permission.CREATE_PORTFOLIO,
        Permission.EDIT_PORTFOLIO,
        Permission.VIEW_PORTFOLIO,
        Permission.MANAGE_PORTFOLIO_MEMBERS,
        Permission.CREATE_PROJECT,
        Permission.EDIT_PROJECT,
        Permission.VIEW_PROJECT,
        Permission.MANAGE_PROJECT_MEMBERS,
        Permission.APPROVE_PROJECT_CHANGES,
        Permission.MANAGE_RESOURCES,
        Permission.VIEW_RESOURCES,
        Permission.ASSIGN_RESOURCES,
        Permission.VIEW_RESOURCE_UTILIZATION,
        Permission.VIEW_BUDGETS,
        Permission.APPROVE_BUDGETS,
        Permission.VIEW_FINANCIAL_REPORTS,
        Permission.APPROVE_TIME,
        Permission.VIEW_TIME_REPORTS,
        Permission.MANAGE_RISKS,
        Permission.VIEW_RISKS,
        Permission.VIEW_REPORTS,
        Permission.CREATE_REPORTS,
        Permission.EXPORT_DATA,
    },
    
    UserRole.PORTFOLIO_MANAGER: {
        # Portfolio oversight and management
        Permission.VIEW_USERS,
        Permission.CREATE_PORTFOLIO,
        Permission.EDIT_PORTFOLIO,
        Permission.VIEW_PORTFOLIO,
        Permission.MANAGE_PORTFOLIO_MEMBERS,
        Permission.CREATE_PROJECT,
        Permission.EDIT_PROJECT,
        Permission.VIEW_PROJECT,
        Permission.MANAGE_PROJECT_MEMBERS,
        Permission.VIEW_RESOURCES,
        Permission.ASSIGN_RESOURCES,
        Permission.VIEW_RESOURCE_UTILIZATION,
        Permission.MANAGE_BUDGETS,
        Permission.VIEW_BUDGETS,
        Permission.VIEW_FINANCIAL_REPORTS,
        Permission.APPROVE_TIME,
        Permission.VIEW_TIME_REPORTS,
        Permission.MANAGE_RISKS,
        Permission.VIEW_RISKS,
        Permission.VIEW_REPORTS,
        Permission.CREATE_REPORTS,
        Permission.EXPORT_DATA,
    },
    
    UserRole.PROJECT_MANAGER: {
        # Project execution and management
        Permission.VIEW_USERS,
        Permission.VIEW_PORTFOLIO,
        Permission.EDIT_PROJECT,
        Permission.VIEW_PROJECT,
        Permission.MANAGE_PROJECT_MEMBERS,
        Permission.VIEW_RESOURCES,
        Permission.ASSIGN_RESOURCES,
        Permission.VIEW_RESOURCE_UTILIZATION,
        Permission.VIEW_BUDGETS,
        Permission.VIEW_FINANCIAL_REPORTS,
        Permission.APPROVE_TIME,
        Permission.VIEW_TIME_REPORTS,
        Permission.MANAGE_RISKS,
        Permission.VIEW_RISKS,
        Permission.VIEW_REPORTS,
        Permission.CREATE_REPORTS,
    },
    
    UserRole.RESOURCE: {
        # Task execution and time tracking
        Permission.VIEW_PROJECT,
        Permission.ENTER_TIME,
        Permission.VIEW_RISKS,
        Permission.VIEW_REPORTS,
    },
    
    UserRole.FINANCE: {
        # Budget oversight and financial tracking
        Permission.VIEW_USERS,
        Permission.VIEW_PORTFOLIO,
        Permission.VIEW_PROJECT,
        Permission.MANAGE_BUDGETS,
        Permission.VIEW_BUDGETS,
        Permission.APPROVE_BUDGETS,
        Permission.VIEW_FINANCIAL_REPORTS,
        Permission.VIEW_TIME_REPORTS,
        Permission.VIEW_RISKS,
        Permission.VIEW_REPORTS,
        Permission.CREATE_REPORTS,
        Permission.EXPORT_DATA,
    },
    
    UserRole.VIEWER: {
        # Read-only access to authorized content
        Permission.VIEW_PORTFOLIO,
        Permission.VIEW_PROJECT,
        Permission.VIEW_RESOURCES,
        Permission.VIEW_BUDGETS,
        Permission.VIEW_RISKS,
        Permission.VIEW_REPORTS,
    }
}

def get_user_permissions(role: UserRole) -> Set[Permission]:
    """Get all permissions for a user role"""
    return ROLE_PERMISSIONS.get(role, set())

def user_has_permission(role: UserRole, permission: Permission) -> bool:
    """Check if user role has a specific permission"""
    user_permissions = get_user_permissions(role)
    return permission in user_permissions

def user_has_any_permission(role: UserRole, permissions: List[Permission]) -> bool:
    """Check if user role has any of the specified permissions"""
    user_permissions = get_user_permissions(role)
    return any(perm in user_permissions for perm in permissions)

def user_has_all_permissions(role: UserRole, permissions: List[Permission]) -> bool:
    """Check if user role has all of the specified permissions"""
    user_permissions = get_user_permissions(role)
    return all(perm in user_permissions for perm in permissions)

class AccessLevel(str, Enum):
    """Access levels for resource-specific permissions"""
    FULL = "full"        # Full read/write access
    READ_WRITE = "read_write"  # Read and write access
    READ_ONLY = "read_only"    # Read-only access
    NO_ACCESS = "no_access"    # No access

def get_resource_access_level(
    user_role: UserRole,
    resource_type: str,
    user_id: str,
    resource_owner_id: str = None,
    portfolio_access: List[str] = None,
    project_access: List[str] = None,
    resource_id: str = None
) -> AccessLevel:
    """
    Determine access level for a specific resource based on role and ownership
    
    Args:
        user_role: User's role
        resource_type: Type of resource (portfolio, project, etc.)
        user_id: Current user's ID
        resource_owner_id: Owner/manager of the resource
        portfolio_access: List of portfolio IDs user has explicit access to
        project_access: List of project IDs user has explicit access to
        resource_id: ID of the specific resource
    
    Returns:
        AccessLevel enum value
    """
    portfolio_access = portfolio_access or []
    project_access = project_access or []
    
    # Admins and PMO Admins have full access to everything
    if user_role in [UserRole.ADMIN, UserRole.PMO_ADMIN]:
        return AccessLevel.FULL
    
    # Portfolio Managers have full access to their portfolios and read access to others
    if user_role == UserRole.PORTFOLIO_MANAGER:
        if resource_type == "portfolio":
            if resource_id in portfolio_access or user_id == resource_owner_id:
                return AccessLevel.FULL
            return AccessLevel.READ_ONLY
        elif resource_type == "project":
            if resource_id in project_access or user_id == resource_owner_id:
                return AccessLevel.READ_WRITE
            return AccessLevel.READ_ONLY
    
    # Project Managers have full access to their projects
    if user_role == UserRole.PROJECT_MANAGER:
        if resource_type == "project":
            if resource_id in project_access or user_id == resource_owner_id:
                return AccessLevel.FULL
            return AccessLevel.READ_ONLY
        elif resource_type == "portfolio":
            return AccessLevel.READ_ONLY
    
    # Finance role has read-write access to financial aspects
    if user_role == UserRole.FINANCE:
        return AccessLevel.READ_WRITE
    
    # Resources have limited access
    if user_role == UserRole.RESOURCE:
        if resource_type == "project" and resource_id in project_access:
            return AccessLevel.READ_WRITE
        return AccessLevel.READ_ONLY
    
    # Viewers have read-only access to authorized resources
    if user_role == UserRole.VIEWER:
        if (resource_type == "portfolio" and resource_id in portfolio_access) or \
           (resource_type == "project" and resource_id in project_access):
            return AccessLevel.READ_ONLY
    
    return AccessLevel.NO_ACCESS</content>
    </file>
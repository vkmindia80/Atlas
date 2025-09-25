from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import asyncio
from .security import decode_token
from .database import get_database

security = HTTPBearer()

async def get_current_user_and_tenant(credentials: HTTPAuthorizationCredentials):
    """Extract user and tenant information from JWT token"""
    token = credentials.credentials
    payload = decode_token(token)
    
    user_id = payload.get("sub")
    tenant_id = payload.get("tenant_id")
    user_role = payload.get("user_role")
    
    if not user_id or not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "user_id": user_id,
        "tenant_id": tenant_id,
        "user_role": user_role
    }

async def get_tenant_from_code(tenant_code: str):
    """Get tenant information from tenant code"""
    db = await get_database()
    tenant_collection = db.get_default_database().tenants
    
    tenant = await tenant_collection.find_one({"code": tenant_code})
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )
    
    if tenant.get("status") != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tenant account is not active"
        )
    
    return tenant

class TenantMiddleware:
    """Middleware to enforce tenant isolation"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            
            # Skip tenant check for public endpoints
            public_paths = ["/docs", "/redoc", "/openapi.json", "/api/v1/auth/login", "/api/v1/auth/register-tenant"]
            if any(request.url.path.startswith(path) for path in public_paths):
                await self.app(scope, receive, send)
                return
            
            # Extract tenant information from token for authenticated requests
            auth_header = request.headers.get("authorization")
            if auth_header and auth_header.startswith("Bearer "):
                try:
                    token = auth_header.split(" ")[1]
                    payload = decode_token(token)
                    tenant_id = payload.get("tenant_id")
                    
                    if tenant_id:
                        # Add tenant_id to request state for use in endpoints
                        scope["state"] = getattr(scope, "state", {})
                        scope["state"]["tenant_id"] = tenant_id
                        
                except Exception:
                    pass  # Let the endpoint handle authentication
            
        await self.app(scope, receive, send)
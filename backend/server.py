from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.core.middleware import TenantMiddleware
from app.api.v1 import auth, users, portfolios, projects, admin
import uvicorn

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AtlasPM - Enterprise Portfolio & Project Management SaaS Platform",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

# Add tenant isolation middleware
app.add_middleware(TenantMiddleware)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal server error",
            "detail": str(exc) if settings.ENVIRONMENT == "development" else "An unexpected error occurred"
        }
    )

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize database connection and create indexes"""
    await connect_to_mongo()
    print(f"🚀 {settings.PROJECT_NAME} v{settings.VERSION} started successfully!")
    print(f"📚 API Documentation: http://localhost:8001/docs")

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connections"""
    await close_mongo_connection()
    print("🛑 AtlasPM shutdown complete")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }

# Include API routes
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["Authentication"])
app.include_router(users.router, prefix=settings.API_V1_STR, tags=["Users"])
app.include_router(portfolios.router, prefix=settings.API_V1_STR, tags=["Portfolios"])
app.include_router(projects.router, prefix=settings.API_V1_STR, tags=["Projects"])
app.include_router(admin.router, prefix=settings.API_V1_STR, tags=["Administration"])

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8001,
        reload=True if settings.ENVIRONMENT == "development" else False
    )
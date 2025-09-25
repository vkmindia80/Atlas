# AtlasPM - Enterprise Portfolio & Project Management SaaS

## Overview
AtlasPM is a comprehensive, multi-tenant SaaS platform designed for enterprise Portfolio and Project Management. Built for large organizations including PMOs, Program Managers, Project Managers, Finance teams, and Resources.

## Architecture
- **Backend**: FastAPI (Python) with multi-tenant architecture
- **Frontend**: React with TypeScript
- **Database**: MongoDB with tenant isolation
- **Cache/Queue**: Redis
- **Authentication**: JWT-based with SSO/SAML support

## Features
- Multi-tenant architecture with secure data isolation
- Role-based access control (7 roles with fine-grained permissions)
- Portfolio management with strategic alignment
- Project lifecycle management with Gantt charts
- Resource management and capacity planning
- Financial tracking and budget management
- Time tracking with approval workflows
- Risk and issue management (RAID logs)
- Document management with versioning
- Comprehensive reporting and analytics
- Third-party integrations (Jira, GitHub, Slack, etc.)

## Roles
1. **Admin**: Platform administration
2. **PMO Admin**: PMO-level administration
3. **Portfolio Manager**: Portfolio oversight and management
4. **Project Manager**: Project execution and management
5. **Resource**: Task execution and time tracking
6. **Finance**: Budget oversight and financial tracking
7. **Viewer**: Read-only access to authorized content

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- MongoDB 5.0+
- Redis 6.0+

### Installation

1. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

2. **Frontend Setup**
```bash
cd frontend
yarn install
yarn start
```

### Environment Configuration
Configure your environment variables in `.env` files for both backend and frontend.

## Development Phases

### Phase 1: Foundation & Core Infrastructure ✅
- Multi-tenant database architecture
- Basic authentication and RBAC
- Core portfolio and project CRUD operations
- Basic user management

### Phase 2: Core Business Modules (In Progress)
- Advanced project management features
- Resource management and capacity planning
- Financial tracking and budget management
- Basic dashboard and reporting

### Phase 3: Advanced Features
- Time tracking with approval workflows
- Risk and issue management
- Document management with versioning
- Advanced project planning (Gantt, dependencies)

### Phase 4: Enterprise Features
- SSO/SAML integration
- Advanced reporting and analytics
- Approval workflow engine
- Comprehensive audit logging

### Phase 5: Integrations & Scalability
- Third-party integrations
- Search functionality
- PWA support
- Performance optimization

### Phase 6: Production Readiness
- CI/CD pipeline
- Load testing
- Infrastructure as code
- Comprehensive documentation

## API Documentation
Once running, access the interactive API documentation at:
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## License
Copyright © 2024 AtlasPM. All rights reserved.
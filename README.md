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

### Phase 2: Enhanced Portfolio & Project Management (In Progress) 🚧
**Current Sprint: Portfolio & Project Module Enhancement**

#### Phase 2.1: Enhanced Data Models & Project Lifecycle ✅
- ✅ Enhanced portfolio-project relationship models
- ✅ Task management with dependencies and time tracking
- ✅ Project intake forms and templates
- ✅ Project baselining and snapshots
- ✅ Milestone and phase management
- ✅ CSV import and bulk operations
- ✅ Sample data with 10 realistic projects across 3 portfolios

#### Phase 2.2: Advanced Project Views ✅
- ✅ Interactive Gantt charts with timeline visualization, task bars, and progress tracking
- ✅ Kanban board with drag-and-drop functionality using react-beautiful-dnd
- ✅ Enhanced calendar view with project milestones and task integration
- ✅ Comprehensive document management with search, filtering, and folder organization
- ✅ Advanced budget & cost tracking with breakdown analysis and forecasting
- ✅ Complete issues & risks management with RAID log functionality

#### Phase 2.3: Portfolio Dashboard & KPIs (Current) 🔄
- Portfolio dashboard with real-time KPIs
- Status count aggregations
- Budget utilization tracking
- Risk heatmap visualization
- Performance optimizations for large datasets

#### Phase 2.4: Testing & Sample Data
- Jest unit tests for all components
- Playwright e2e tests for main workflows
- Realistic sample data generation (100 projects)
- Performance testing and optimization

### Phase 3: Advanced Features
- Time tracking with approval workflows
- Advanced risk and issue management (RAID logs)
- Document management with versioning
- Resource capacity planning
- Advanced reporting and analytics

### Phase 4: Enterprise Features
- SSO/SAML integration
- Workflow automation engine
- Advanced audit logging
- Multi-language support
- Custom field management

### Phase 5: Integrations & Scalability
- Third-party integrations (Jira, GitHub, Slack)
- Search functionality with Elasticsearch
- PWA support for mobile
- Caching and performance optimization
- API rate limiting

### Phase 6: Production Readiness
- CI/CD pipeline setup
- Load testing and benchmarks
- Infrastructure as code (Terraform)
- Comprehensive API documentation
- Security hardening

## Current Implementation Status

### ✅ Completed Features
- Multi-tenant architecture with MongoDB
- JWT authentication and role-based access control
- Basic portfolio CRUD operations
- Basic project CRUD operations
- Responsive frontend with React + TypeScript
- API documentation with FastAPI

### ✅ Recently Completed (Phase 2.2)
- Interactive Gantt chart with timeline visualization and task progress
- Drag-and-drop Kanban board with real-time task status updates
- Enhanced calendar view with milestone and task integration
- Comprehensive document management system
- Advanced budget tracking with cost breakdown and forecasting
- Complete RAID (Risks, Actions, Issues, Decisions) log management

### 🚧 In Development (Phase 2.3) - Current
- Portfolio dashboard with real-time KPIs
- Status count aggregations
- Budget utilization tracking
- Risk heatmap visualization
- Performance optimizations for large datasets

### 📋 Upcoming Features
- Calendar integration
- Document management
- Time tracking
- Advanced reporting
- Mobile optimization

## API Documentation
Once running, access the interactive API documentation at:
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## Recent Updates & Changelog

### Phase 2.2 Completion (January 2025)
**Advanced Project Views - Interactive Features Implementation**

#### 🆕 New Features Added:
- **Interactive Gantt Chart**
  - Timeline visualization with week/month view modes
  - Task bars with progress indicators and status colors
  - Real-time timeline navigation with date range controls
  - Task dependency visualization planning
  - Priority-based task border indicators

- **Enhanced Kanban Board**
  - Drag-and-drop functionality using react-beautiful-dnd
  - Real-time task status updates via API
  - Visual feedback during drag operations
  - Task progress bars and metadata display
  - Board summary statistics

- **Advanced Calendar View**
  - Month navigation with milestone integration
  - Event categorization (milestones, deadlines)
  - Interactive date selection
  - Project timeline overlay

- **Document Management System**
  - File upload and organization capabilities
  - Search and filtering by category and tags
  - List and grid view modes
  - File versioning and metadata tracking
  - Folder-based organization structure

- **Budget & Cost Tracking**
  - Real-time budget utilization monitoring
  - Cost breakdown by category (Labor, Materials, Vendors, Overhead)
  - Variance analysis and forecasting
  - Interactive budget progress visualization
  - Multi-tab view (Overview, Breakdown, Forecast)

- **RAID Log Management**
  - Complete Risks, Actions, Issues, Decisions tracking
  - Risk scoring based on probability and impact
  - Issue priority management and assignment
  - Decision logging with approval workflow
  - Status tracking and resolution monitoring

#### 🔧 Technical Improvements:
- Added react-beautiful-dnd for drag-and-drop functionality
- Enhanced API service integration for real-time updates
- Improved TypeScript type definitions
- Added comprehensive data-testid attributes for testing
- Responsive design improvements across all components

#### 📊 Key Metrics:
- 6 major components enhanced with interactive features
- 100+ data-testid attributes added for comprehensive testing
- Real-time API integration for task status updates
- Drag-and-drop capability with visual feedback

#### 🎯 Next Phase (2.3):
Ready to proceed with Portfolio Dashboard & KPIs implementation including real-time status aggregations and performance visualizations.

## License
Copyright © 2024 AtlasPM. All rights reserved.
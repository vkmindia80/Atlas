# AtlasPM Architecture Specification

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Service Descriptions](#service-descriptions)
4. [Data Architecture](#data-architecture)
5. [Authentication & Authorization](#authentication--authorization)
6. [SSO Integration](#sso-integration)
7. [SCIM Provisioning](#scim-provisioning)
8. [API Architecture](#api-architecture)
9. [Database Design](#database-design)
10. [Performance & Scalability](#performance--scalability)
11. [Security Architecture](#security-architecture)
12. [Integration Architecture](#integration-architecture)
13. [Monitoring & Observability](#monitoring--observability)
14. [Deployment Architecture](#deployment-architecture)

## Overview

AtlasPM is a comprehensive, multi-tenant SaaS platform designed for enterprise Portfolio and Project Management. The platform serves large organizations including PMOs, Program Managers, Project Managers, Finance teams, and Resources with sophisticated portfolio management capabilities, advanced project tracking, resource management, financial oversight, and comprehensive reporting.

### Key Characteristics

- **Multi-Tenant Architecture**: Complete tenant isolation with shared infrastructure
- **Enterprise-Grade**: SSO/SAML integration, SCIM provisioning, advanced RBAC
- **Scalable**: Designed to handle thousands of users and projects per tenant
- **Real-Time**: WebSocket connections for live updates and notifications
- **API-First**: Comprehensive REST API with webhook integrations
- **Audit-Complete**: Full audit trail for compliance and governance

### Technology Stack

- **Frontend**: React 18+ with TypeScript, Tailwind CSS, React Query
- **Backend**: FastAPI (Python 3.9+) with Pydantic validation
- **Database**: MongoDB 5.0+ with multi-tenant collections
- **Cache/Queue**: Redis 6.0+ for caching and background jobs
- **Task Queue**: Celery for asynchronous processing
- **Search**: Elasticsearch for full-text search capabilities
- **Authentication**: JWT with SSO/SAML support
- **File Storage**: AWS S3 compatible storage
- **Monitoring**: OpenTelemetry, Prometheus, Grafana

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           AtlasPM Platform                         │
├─────────────────────────────────────────────────────────────────────┤
│                          Load Balancer                             │
├─────────────────────────────────────────────────────────────────────┤
│  Web App      │  API Gateway  │  Admin Portal │  Integration APIs  │
│  (React)      │  (FastAPI)    │  (React)      │  (FastAPI)        │
├─────────────────────────────────────────────────────────────────────┤
│             Application Services Layer                              │
├─────────────────────────────────────────────────────────────────────┤
│ Portfolio     │ Project Mgmt  │ Task Mgmt     │ Resource Mgmt     │
│ Management    │ Service       │ Service       │ Service           │
├─────────────────────────────────────────────────────────────────────┤
│ Time Tracking │ Budget Mgmt   │ Risk Mgmt     │ Document Mgmt     │
│ Service       │ Service       │ Service       │ Service           │
├─────────────────────────────────────────────────────────────────────┤
│ Workflow      │ Notification  │ Reporting     │ Integration       │
│ Engine        │ Service       │ Service       │ Service           │
├─────────────────────────────────────────────────────────────────────┤
│                     Infrastructure Services                         │
├─────────────────────────────────────────────────────────────────────┤
│ Auth Service  │ Search Service│ File Service  │ Audit Service     │
│ (JWT/SSO)     │ (Elasticsearch)│ (S3)         │ (Compliance)      │
├─────────────────────────────────────────────────────────────────────┤
│                         Data Layer                                  │
├─────────────────────────────────────────────────────────────────────┤
│   MongoDB     │    Redis      │ Elasticsearch │   File Storage    │
│ (Primary DB)  │ (Cache/Queue) │  (Search)     │    (S3/MinIO)     │
└─────────────────────────────────────────────────────────────────────┘
```

## Service Descriptions

### 1. Web Application (React Frontend)

**Purpose**: Primary user interface for end users
- **Technology**: React 18+ with TypeScript, Tailwind CSS
- **Features**: 
  - Responsive dashboard interfaces
  - Portfolio and project management UI
  - Task tracking and time entry
  - Budget and cost management
  - Risk management (RAID logs)
  - Real-time notifications
  - Advanced reporting and analytics
- **Authentication**: JWT tokens with automatic refresh
- **State Management**: React Query for server state, Context API for global state

### 2. API Service (FastAPI Backend)

**Purpose**: Core business logic and data management
- **Technology**: FastAPI with Python 3.9+, Pydantic for validation
- **Architecture**: 
  - Layered architecture (Controller → Service → Repository)
  - Multi-tenant aware middleware
  - Comprehensive input validation and sanitization
  - Automatic API documentation generation
- **Capabilities**:
  - Full CRUD operations for all entities
  - Complex business logic processing
  - Multi-tenant data isolation
  - Advanced search and filtering
  - Bulk operations support
  - Webhook management

### 3. Authentication Service

**Purpose**: Centralized authentication and authorization
- **Technology**: JWT with RS256 signing, SSO/SAML integration
- **Features**:
  - Multi-tenant user authentication
  - Role-based access control (RBAC)
  - SSO integration (Azure AD, Okta, Google Workspace)
  - SCIM provisioning for enterprise identity management
  - Session management and security
  - Password policies and MFA support

### 4. Worker Queue Service

**Purpose**: Background processing and asynchronous tasks
- **Technology**: Celery with Redis broker
- **Responsibilities**:
  - Email and notification sending
  - Report generation and export
  - Data synchronization with external systems
  - File processing and virus scanning
  - Bulk operations processing
  - Scheduled tasks (reminders, alerts, reports)

### 5. Search Service

**Purpose**: Full-text search and advanced filtering
- **Technology**: Elasticsearch with custom analyzers
- **Capabilities**:
  - Global search across all entities
  - Faceted search with filters
  - Auto-complete and suggestion features
  - Search result ranking and relevance
  - Real-time index updates
  - Multi-tenant search isolation

### 6. Notification Service

**Purpose**: Multi-channel notification delivery
- **Technology**: Event-driven architecture with multiple delivery channels
- **Channels**:
  - In-app notifications (WebSocket)
  - Email notifications (SendGrid/SES)
  - SMS notifications (Twilio)
  - Mobile push notifications
  - Webhook notifications to external systems
- **Features**:
  - Template-based messaging
  - Notification preferences and scheduling
  - Delivery tracking and retry logic

## Data Architecture

### Entity Relationship Overview

The AtlasPM data model is built around a hierarchical multi-tenant architecture:

```
Tenant (Organization)
├── Organizations (Departments/Units)
│   ├── Users (Team Members)
│   └── Portfolios (Strategic Initiatives)
│       └── Projects (Execution Units)
│           └── Tasks (Work Items)
│               ├── Assignments (Resource Allocation)
│               └── Timesheets (Time Tracking)
├── Budgets (Financial Planning)
│   └── Costs (Expense Tracking)
├── Risks (Risk Management)
├── Workflows (Approval Processes)
├── Attachments (Document Management)
├── Notifications (Communication)
├── Reports (Analytics)
└── Audit Logs (Compliance)
```

### Core Collections

#### 1. **tenants**
- **Purpose**: Root organization entities
- **Key Fields**: name, code, domain, subscription details, settings
- **Relationships**: One-to-many with all other collections
- **Indexing**: Unique indexes on code and domain

#### 2. **organizations**
- **Purpose**: Departmental/organizational hierarchy
- **Key Fields**: name, parent_org_id, org_level, manager_id
- **Relationships**: Self-referential hierarchy, one-to-many users/portfolios
- **Indexing**: Hierarchical path index for efficient tree queries

#### 3. **users**
- **Purpose**: System users with RBAC
- **Key Fields**: username, email, role, status, permissions
- **Relationships**: Belongs to tenant/organization, manages portfolios/projects
- **Indexing**: Unique composite indexes on tenant+username/email

#### 4. **portfolios**
- **Purpose**: Strategic portfolio management
- **Key Fields**: name, type, status, financial_metrics, strategic_objectives
- **Relationships**: Contains projects, managed by users
- **Indexing**: Multi-field indexes for filtering and reporting

#### 5. **projects** 
- **Purpose**: Project execution management
- **Key Fields**: name, type, methodology, status, timeline, financials
- **Relationships**: Belongs to portfolio, contains tasks
- **Indexing**: Date range indexes for timeline queries

#### 6. **tasks**
- **Purpose**: Work item tracking
- **Key Fields**: name, type, status, assignee, estimates, actuals
- **Relationships**: Belongs to project, has assignments and timesheets
- **Indexing**: Assignee and due date indexes for workload management

### Advanced Collections

#### 7. **timesheets**
- **Purpose**: Time tracking with approval workflows
- **Key Fields**: user_id, task_id, hours, status, approver_id
- **Business Logic**: Approval workflows, cost calculations
- **Archiving**: Monthly archiving for performance

#### 8. **budgets** & **costs**
- **Purpose**: Financial management and tracking
- **Key Fields**: budget amounts, cost categories, approval status
- **Reporting**: Real-time budget vs. actual analysis
- **Compliance**: Audit trail for financial changes

#### 9. **risks**
- **Purpose**: RAID (Risks, Actions, Issues, Decisions) logs
- **Key Fields**: type, category, probability, impact, mitigation
- **Analytics**: Risk scoring and escalation rules

#### 10. **workflows** & **workflow_instances**
- **Purpose**: Configurable approval and automation processes
- **Key Fields**: workflow definitions, execution state, approvals
- **Engine**: Rule-based workflow execution with escalations

## Authentication & Authorization

### JWT Token Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client App    │    │  Auth Service   │    │  Resource API   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │  1. Login Request     │                       │
         ├──────────────────────>│                       │
         │                       │                       │
         │  2. JWT Tokens        │                       │
         │<──────────────────────┤                       │
         │                       │                       │
         │  3. API Request       │                       │
         │  (Bearer Token)       │                       │
         ├───────────────────────────────────────────────>│
         │                       │                       │
         │                       │  4. Token Validation  │
         │                       │<──────────────────────┤
         │                       │                       │
         │  5. API Response      │                       │
         │<───────────────────────────────────────────────┤
```

### Token Structure

**Access Token Claims:**
```json
{
  "sub": "user_id",
  "tenant_id": "tenant_uuid",
  "role": "project_manager", 
  "permissions": ["project.read", "task.create"],
  "org_id": "org_uuid",
  "exp": 1640995200,
  "iat": 1640991600,
  "token_type": "access"
}
```

**Refresh Token Claims:**
```json
{
  "sub": "user_id",
  "tenant_id": "tenant_uuid", 
  "exp": 1648771200,
  "iat": 1640991600,
  "token_type": "refresh"
}
```

### Role-Based Access Control (RBAC)

#### 1. **Admin**
- Platform-level administration
- Full access to all tenant resources
- User management and system configuration

#### 2. **PMO Admin** 
- PMO-level administration within tenant
- Portfolio oversight and governance
- Advanced reporting and analytics

#### 3. **Portfolio Manager**
- Portfolio management and strategic alignment
- Cross-project resource allocation
- Portfolio-level reporting

#### 4. **Project Manager**
- Project execution and team management  
- Task assignment and progress tracking
- Project-level budget and timeline management

#### 5. **Resource**
- Task execution and time tracking
- Personal dashboard and notifications
- Limited project visibility

#### 6. **Finance**
- Budget oversight and cost tracking
- Financial reporting and analysis
- Approval of budget-related requests

#### 7. **Viewer**
- Read-only access to authorized content
- Dashboard viewing and report access
- No modification permissions

### Permission Matrix

| Resource | Admin | PMO Admin | Portfolio Mgr | Project Mgr | Resource | Finance | Viewer |
|----------|-------|-----------|---------------|-------------|----------|---------|--------|
| Tenants | CRUD | R | R | R | R | R | R |
| Users | CRUD | CRU | R | R | R | R | R |
| Portfolios | CRUD | CRUD | CRUD (owned) | R | R | R | R |
| Projects | CRUD | CRUD | CRUD | CRUD (owned) | R (assigned) | R | R |
| Tasks | CRUD | CRUD | CRUD | CRUD | CRU (assigned) | R | R |
| Timesheets | CRUD | CRUD | R | RU | CRUD (own) | R | R |
| Budgets | CRUD | CRUD | CRUD | RU | R | CRUD | R |
| Reports | CRUD | CRUD | CRUD | CRU | R | CRUD | R |

## SSO Integration

### Supported Identity Providers

#### 1. **Azure Active Directory / Microsoft 365**
- **Protocol**: SAML 2.0, OpenID Connect
- **Features**: 
  - Single sign-on with Microsoft accounts
  - Automatic user provisioning via SCIM
  - Multi-factor authentication support
  - Conditional access policies

#### 2. **Okta**
- **Protocol**: SAML 2.0, OpenID Connect  
- **Features**:
  - Universal directory integration
  - Advanced user lifecycle management
  - Adaptive authentication
  - API access management

#### 3. **Google Workspace**
- **Protocol**: SAML 2.0, OAuth 2.0
- **Features**:
  - Google SSO integration
  - G Suite user synchronization
  - Context-aware access
  - Security investigation tools

#### 4. **Generic SAML 2.0**
- **Protocol**: SAML 2.0
- **Features**:
  - Standards-compliant SAML implementation
  - Configurable attribute mapping
  - Support for encrypted assertions
  - Multiple certificate management

### SSO Authentication Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    User     │    │  AtlasPM    │    │ Identity    │    │  AtlasPM    │
│             │    │  Frontend   │    │ Provider    │    │  Backend    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                  │                  │                  │
       │ 1. Access App    │                  │                  │
       ├─────────────────>│                  │                  │
       │                  │                  │                  │
       │ 2. Redirect to   │                  │                  │
       │    IdP Login     │                  │                  │
       │<─────────────────┤                  │                  │
       │                  │                  │                  │
       │ 3. Authenticate  │                  │                  │
       ├─────────────────────────────────────>│                  │
       │                  │                  │                  │
       │ 4. SAML Response │                  │                  │
       │<─────────────────────────────────────┤                  │
       │                  │                  │                  │
       │ 5. Post to       │                  │                  │
       │    AtlasPM       │                  │                  │
       ├─────────────────>│                  │                  │
       │                  │                  │                  │
       │                  │ 6. Verify SAML  │                  │
       │                  │ & Create Session │                  │
       │                  ├─────────────────────────────────────>│
       │                  │                  │                  │
       │                  │ 7. JWT Tokens    │                  │
       │                  │<─────────────────────────────────────┤
       │                  │                  │                  │
       │ 8. App Dashboard │                  │                  │
       │<─────────────────┤                  │                  │
```

## SCIM Provisioning

### SCIM 2.0 Implementation

AtlasPM provides a complete SCIM 2.0 implementation for automated user lifecycle management from enterprise identity systems.

#### Supported Resources

**Users Resource (`/scim/v2/Users`)**
- User creation, modification, and deactivation
- Attribute mapping and transformation
- Password management (when applicable)
- Group membership management

**Groups Resource (`/scim/v2/Groups`)**
- Organization and team synchronization
- Role-based group mapping
- Nested group support
- Membership management

#### SCIM User Schema Mapping

```json
{
  "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
  "id": "user_uuid",
  "externalId": "external_id_from_idp", 
  "userName": "john.doe@company.com",
  "name": {
    "givenName": "John",
    "familyName": "Doe",
    "formatted": "John Doe"
  },
  "emails": [
    {
      "value": "john.doe@company.com",
      "primary": true
    }
  ],
  "active": true,
  "roles": ["project_manager"],
  "enterprise": {
    "employeeNumber": "12345",
    "department": "Engineering",
    "manager": {
      "value": "manager_user_id"
    }
  }
}
```

#### Provisioning Operations

1. **Create User**: Automatic user creation with role assignment
2. **Update User**: Profile updates and role changes  
3. **Deactivate User**: User account suspension
4. **Delete User**: Account removal (soft delete)
5. **Bulk Operations**: Efficient batch processing

### Enterprise Integration Patterns

#### Attribute Mapping Configuration

```yaml
scim_mapping:
  user_attributes:
    userName: email
    givenName: first_name  
    familyName: last_name
    emails[primary]: email
    active: is_active
    enterprise.department: department
    enterprise.employeeNumber: employee_id
  
  custom_attributes:
    cost_center: "urn:custom:cost_center"
    job_title: "urn:custom:title" 
    hourly_rate: "urn:custom:rate"
  
  role_mapping:
    "AtlasPM_Admin": "admin"
    "AtlasPM_PMO": "pmo_admin" 
    "AtlasPM_PM": "project_manager"
    "AtlasPM_Resource": "resource"
```

## API Architecture

### RESTful Design Principles

- **Resource-based URLs**: `/api/v1/projects/{id}` 
- **HTTP Methods**: GET, POST, PUT, DELETE, PATCH
- **Status Codes**: Proper HTTP status code usage
- **Content Negotiation**: JSON primary, CSV/Excel for exports
- **Versioning**: URL path versioning (`/api/v1/`, `/api/v2/`)

### Request/Response Patterns

#### Standard Response Format

```json
{
  "data": {}, // or [] for collections
  "meta": {
    "page": 1,
    "limit": 20, 
    "total": 150,
    "has_next": true
  },
  "links": {
    "self": "/api/v1/projects?page=1",
    "next": "/api/v1/projects?page=2",
    "prev": null
  }
}
```

#### Error Response Format

```json
{
  "error": "validation_error",
  "message": "Invalid request data",
  "details": {
    "field_errors": {
      "name": ["This field is required"],
      "email": ["Invalid email format"]
    }
  },
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/api/v1/users",
  "request_id": "req_12345"
}
```

### Advanced API Features

#### 1. **Filtering and Search**
```
GET /api/v1/projects?status=active&manager_id=123&search=mobile
GET /api/v1/tasks?assignee_id=456&due_date_from=2024-01-01&due_date_to=2024-01-31
```

#### 2. **Field Selection**
```  
GET /api/v1/projects?fields=id,name,status,manager_name
```

#### 3. **Sorting**
```
GET /api/v1/projects?sort=name,created_at&order=asc,desc
```

#### 4. **Bulk Operations**
```json
POST /api/v1/bulk/tasks
{
  "operation": "create",
  "data": [
    {"name": "Task 1", "project_id": "123"},
    {"name": "Task 2", "project_id": "123"}
  ]
}
```

#### 5. **Async Operations**
```json  
POST /api/v1/reports/generate
{
  "type": "portfolio_summary",
  "parameters": {...}
}
Response: 202 Accepted
{
  "job_id": "job_12345",
  "status": "processing", 
  "status_url": "/api/v1/jobs/job_12345"
}
```

### Webhook Architecture

#### Event Types

- **Entity Events**: `project.created`, `task.updated`, `user.deleted`
- **Workflow Events**: `approval.requested`, `workflow.completed`
- **Time Events**: `timesheet.submitted`, `timesheet.approved`
- **Budget Events**: `budget.exceeded`, `cost.approved`

#### Webhook Payload Format

```json
{
  "event_type": "project.created",
  "event_id": "evt_12345",
  "tenant_id": "tenant_123", 
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "project": {
      "id": "proj_456",
      "name": "New Mobile App",
      "status": "active"
    }
  },
  "previous_data": null
}
```

#### Webhook Security

- **Signature Verification**: HMAC-SHA256 signatures
- **Retry Logic**: Exponential backoff with 5 retry attempts
- **Timeout Handling**: 30-second timeout per request
- **IP Allowlisting**: Optional IP restriction

## Database Design

### MongoDB Collection Strategy

#### Multi-Tenant Isolation

**Collection-Level Isolation**: All collections include `tenant_id` as the first field in every document and index. This ensures:
- Complete data separation between tenants
- Efficient querying with tenant-scoped indexes  
- Simplified backup and recovery per tenant
- Clear audit trails

#### Document Structure Standards

```javascript
// Base document structure
{
  "_id": "uuid_string", // UUID instead of ObjectId for JSON compatibility
  "tenant_id": "tenant_uuid", // Always first field for indexing
  "org_id": "org_uuid", // Organizational hierarchy
  // Entity-specific fields
  "is_active": true, // Soft delete flag
  "created_at": ISODate(), 
  "updated_at": ISODate(),
  "created_by": "user_uuid",
  "updated_by": "user_uuid",
  "metadata": {} // Extensible metadata object
}
```

### Indexing Strategy

#### Primary Indexes (All Collections)

```javascript
// Tenant isolation index (most important)
db.collection.createIndex({"tenant_id": 1})

// Composite indexes for common queries  
db.users.createIndex({"tenant_id": 1, "username": 1}, {unique: true})
db.users.createIndex({"tenant_id": 1, "email": 1}, {unique: true})

// Status and filtering indexes
db.projects.createIndex({"tenant_id": 1, "status": 1})
db.projects.createIndex({"tenant_id": 1, "portfolio_id": 1})

// Date-based queries (timeline, reporting)
db.timesheets.createIndex({"tenant_id": 1, "date": 1})
db.tasks.createIndex({"tenant_id": 1, "due_date": 1})

// Full-text search
db.projects.createIndex({
  "tenant_id": 1,
  "name": "text", 
  "description": "text"
})
```

#### Performance Indexes

```javascript
// Hierarchical queries
db.organizations.createIndex({"tenant_id": 1, "parent_org_id": 1})
db.tasks.createIndex({"tenant_id": 1, "parent_task_id": 1})

// Assignment and workload queries
db.assignments.createIndex({"tenant_id": 1, "user_id": 1, "status": 1})
db.timesheets.createIndex({"tenant_id": 1, "user_id": 1, "date": -1})

// Budget and financial reporting
db.costs.createIndex({"tenant_id": 1, "project_id": 1, "cost_date": -1})
db.budgets.createIndex({"tenant_id": 1, "fiscal_year": 1, "status": 1})
```

### Data Archiving Strategy

#### Large Table Management

**Timesheets Collection**
- **Growth Rate**: ~1M records/month for 1000 active users
- **Archiving**: Monthly archiving after 13 months retention
- **Archive Strategy**: Move to `timesheets_archive_YYYY` collections
- **Access Pattern**: Recent data in main collection, archived data for reporting only

**Audit Logs Collection**
- **Growth Rate**: ~10M records/month for active tenant
- **Retention**: 7 years for compliance requirements
- **Partitioning**: Monthly collections `audit_logs_YYYY_MM`
- **TTL Index**: Automatic deletion after retention period

**Costs Collection**
- **Growth Rate**: ~100K records/month per tenant
- **Archiving**: Quarterly archiving after 2 years
- **Compression**: High compression for archived data

#### Archive Implementation

```javascript
// TTL Index for automatic cleanup
db.audit_logs.createIndex(
  {"timestamp": 1}, 
  {"expireAfterSeconds": 220752000} // 7 years
)

// Archiving procedure (monthly job)
function archiveTimesheets(cutoffDate) {
  const archiveCollection = `timesheets_archive_${cutoffDate.getFullYear()}`;
  
  // Move old records to archive collection
  db.timesheets.aggregate([
    {$match: {"created_at": {$lt: cutoffDate}}},
    {$out: archiveCollection}
  ]);
  
  // Remove from main collection
  db.timesheets.deleteMany({"created_at": {$lt: cutoffDate}});
  
  // Create indexes on archive collection
  db[archiveCollection].createIndex({"tenant_id": 1, "user_id": 1});
}
```

### Backup and Recovery Strategy

#### Backup Strategy
- **Frequency**: Daily incremental, weekly full backups
- **Retention**: 30 days online, 1 year archived, 7 years compliance
- **Tenant Isolation**: Per-tenant backup capability for data sovereignty
- **Point-in-Time**: 5-minute granularity for critical data recovery

#### Disaster Recovery
- **RTO**: 4 hours maximum downtime
- **RPO**: 15 minutes maximum data loss  
- **Multi-Region**: Active-passive setup with automated failover
- **Testing**: Monthly DR drills and quarterly full tests

## Performance & Scalability  

### Horizontal Scaling Architecture

```
                    ┌─────────────────┐
                    │  Load Balancer  │
                    └─────────────────┘
                             │
                    ┌─────────────────┐
                    │   API Gateway   │ 
                    └─────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
    ┌─────────┐         ┌─────────┐         ┌─────────┐
    │FastAPI-1│         │FastAPI-2│         │FastAPI-3│
    └─────────┘         └─────────┘         └─────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                ┌─────────────────────────┐
                │      MongoDB Cluster   │
                │  (Sharded/Replica Set)  │
                └─────────────────────────┘
```

### Database Scaling Patterns

#### MongoDB Sharding Strategy

```javascript
// Shard key design for tenant isolation
sh.shardCollection("atlaspm.users", {"tenant_id": 1, "_id": 1})
sh.shardCollection("atlaspm.projects", {"tenant_id": 1, "created_at": 1})
sh.shardCollection("atlaspm.timesheets", {"tenant_id": 1, "date": 1})

// Zone sharding for geographic data locality
sh.addShardToZone("shard01", "us-east")
sh.addShardToZone("shard02", "us-west")  
sh.addShardToZone("shard03", "eu-west")

sh.addTagRange(
  "atlaspm.users",
  {"tenant_id": MinKey}, 
  {"tenant_id": MaxKey},
  "us-east"
)
```

#### Read Replica Strategy

```javascript
// Read preferences for different operations
const readPreferences = {
  // Real-time operations - primary only
  userAuth: {readPreference: "primary"},
  criticalWrites: {readPreference: "primary"},
  
  // Analytics and reporting - secondary acceptable
  dashboardData: {readPreference: "secondaryPreferred"},
  reportGeneration: {readPreference: "secondary"},
  
  // Search operations - any available
  globalSearch: {readPreference: "nearest"}
}
```

### Caching Strategy

#### Redis Cache Layers

```
┌─────────────────────────────────────────────────┐
│                Application Layer                │
├─────────────────────────────────────────────────┤
│              L1 Cache (In-Memory)               │
│           • User sessions (5 min)               │
│           • Permission cache (10 min)           │
├─────────────────────────────────────────────────┤
│               L2 Cache (Redis)                  │
│           • API responses (30 min)              │
│           • Database query results (1 hour)     │
│           • Dashboard data (15 min)             │
├─────────────────────────────────────────────────┤
│                Database Layer                   │
│                   MongoDB                       │
└─────────────────────────────────────────────────┘
```

#### Cache Keys Strategy

```python
# Hierarchical cache key structure
cache_keys = {
    "user_session": "session:{tenant_id}:{user_id}",
    "user_permissions": "perms:{tenant_id}:{user_id}",
    "dashboard_data": "dash:{tenant_id}:{user_id}:{date}",
    "project_summary": "proj_sum:{tenant_id}:{project_id}",
    "portfolio_metrics": "port_metrics:{tenant_id}:{portfolio_id}"
}

# Cache invalidation patterns
invalidation_patterns = {
    "user_update": ["session:{tenant_id}:{user_id}", "perms:{tenant_id}:{user_id}"],
    "project_update": ["proj_sum:{tenant_id}:{project_id}", "dash:{tenant_id}:*"],
    "timesheet_submit": ["dash:{tenant_id}:*", "proj_sum:{tenant_id}:{project_id}"]
}
```

### Performance Optimization

#### Query Optimization

```python
# Efficient pagination with cursor-based approach
async def get_projects_paginated(tenant_id: str, cursor: str = None, limit: int = 20):
    query = {"tenant_id": tenant_id, "is_active": True}
    
    if cursor:
        cursor_data = decode_cursor(cursor)
        query["created_at"] = {"$lt": cursor_data["created_at"]}
    
    # Use projection to limit data transfer
    projection = {
        "name": 1, "status": 1, "manager_name": 1, 
        "created_at": 1, "progress": 1
    }
    
    projects = await projects_collection.find(query, projection) \
        .sort("created_at", -1) \
        .limit(limit + 1) \
        .to_list(length=None)
    
    has_next = len(projects) > limit
    if has_next:
        projects = projects[:-1]
        
    return {
        "data": projects,
        "has_next": has_next,
        "next_cursor": encode_cursor(projects[-1]) if has_next else None
    }
```

#### Aggregation Pipeline Optimization

```javascript
// Efficient dashboard metrics aggregation
db.projects.aggregate([
  // Stage 1: Match tenant and filter
  {$match: {
    "tenant_id": "tenant_123",
    "status": {$in: ["active", "on_hold"]},
    "created_at": {$gte: ISODate("2024-01-01")}
  }},
  
  // Stage 2: Group by status for counts  
  {$group: {
    "_id": "$status",
    "count": {$sum: 1},
    "total_budget": {$sum: "$financials.total_budget"},
    "avg_progress": {$avg: "$percent_complete"}
  }},
  
  // Stage 3: Add computed fields
  {$addFields: {
    "status": "$_id",
    "budget_millions": {$divide: ["$total_budget", 1000000]}
  }},
  
  // Use indexes: {"tenant_id": 1, "status": 1, "created_at": 1}
], {allowDiskUse: false}) // Ensure memory-only operation
```

### Load Testing Benchmarks

#### Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| API Response Time | <200ms (95th percentile) | Application endpoints |
| Database Query Time | <100ms (average) | MongoDB operations |
| Dashboard Load Time | <2s (complete render) | Frontend performance |
| Concurrent Users | 10,000+ per instance | Load testing |
| Throughput | 5,000 requests/second | Peak load capacity |
| Memory Usage | <4GB per API instance | Resource monitoring |
| CPU Usage | <70% under normal load | Resource monitoring |

#### Scaling Thresholds

```yaml
scaling_triggers:
  api_servers:
    scale_out: 
      - cpu_usage > 70% for 5 minutes
      - memory_usage > 3GB for 3 minutes
      - response_time_p95 > 500ms for 2 minutes
    
  database:
    scale_out:
      - connection_pool > 80% for 10 minutes
      - disk_io > 80% for 15 minutes
      - query_time_avg > 200ms for 5 minutes
    
  redis_cache:
    scale_out:
      - memory_usage > 80%
      - cache_hit_rate < 85%
      - eviction_rate > 100/minute
```

## Security Architecture

### Multi-Layer Security Model

```
┌─────────────────────────────────────────────────┐
│            Application Security Layer           │
│  • Input validation & sanitization             │
│  • Output encoding & XSS prevention            │
│  • CSRF protection & rate limiting             │
├─────────────────────────────────────────────────┤
│           Authentication & Authorization        │
│  • JWT token validation & expiry               │
│  • Role-based access control (RBAC)            │
│  • Multi-factor authentication (MFA)           │
├─────────────────────────────────────────────────┤
│              Transport Security                 │
│  • TLS 1.3 encryption in transit              │
│  • Certificate pinning & HSTS                  │
│  • Secure WebSocket connections                │
├─────────────────────────────────────────────────┤
│               Data Security                     │
│  • Encryption at rest (AES-256)               │
│  • Field-level encryption for PII              │
│  • Key rotation and management                  │
├─────────────────────────────────────────────────┤
│            Infrastructure Security              │
│  • Network segmentation & firewalls            │
│  • Container security & image scanning         │
│  • Vulnerability management                     │
└─────────────────────────────────────────────────┘
```

### Data Protection & Privacy

#### Encryption Strategy

**Data at Rest**
- Database: MongoDB encryption with customer-managed keys
- File Storage: S3 server-side encryption (SSE-KMS)
- Backups: Encrypted backup storage with separate key management
- Application Logs: Encrypted log storage with PII redaction

**Data in Transit**  
- API Communications: TLS 1.3 with perfect forward secrecy
- Database Connections: TLS encrypted MongoDB connections
- Inter-service: mTLS for service-to-service communication
- CDN: HTTPS with HSTS and certificate transparency

#### Personal Data Handling

```python
# PII encryption for sensitive fields
class PIIField:
    def __init__(self, value: str):
        self.encrypted_value = encrypt_pii(value)
        
    def decrypt(self, user_context: UserContext) -> str:
        if not user_context.can_access_pii():
            raise PermissionError("No PII access permission")
        return decrypt_pii(self.encrypted_value)

# Data retention and deletion
async def delete_user_data(user_id: str, tenant_id: str):
    """GDPR-compliant user data deletion"""
    
    # Anonymize audit logs (retain for compliance)
    await audit_logs.update_many(
        {"tenant_id": tenant_id, "user_id": user_id},
        {"$set": {"user_id": "deleted_user", "pii_data": {}}}
    )
    
    # Delete personal data
    await users.delete_one({"_id": user_id, "tenant_id": tenant_id})
    
    # Update references to maintain referential integrity
    await timesheets.update_many(
        {"tenant_id": tenant_id, "user_id": user_id},
        {"$set": {"user_id": "deleted_user"}}
    )
```

### Vulnerability Management

#### Security Headers Implementation

```python
# FastAPI security middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    
    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY" 
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' cdn.atlaspm.com; "
        "style-src 'self' 'unsafe-inline' fonts.googleapis.com; "
        "img-src 'self' data: https:;"
    )
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    return response
```

#### Input Validation & Sanitization

```python
# Comprehensive input validation
class ProjectCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, regex=r'^[a-zA-Z0-9\s\-_\.]+$')
    description: Optional[str] = Field(None, max_length=2000)
    project_type: ProjectType
    
    @validator('name')
    def validate_name(cls, v):
        # XSS prevention
        sanitized = html.escape(v.strip())
        if sanitized != v.strip():
            raise ValueError('Invalid characters detected')
        return sanitized
    
    @validator('description')  
    def validate_description(cls, v):
        if v is None:
            return v
        # Allow basic markdown but escape HTML
        return markdown_escape(v)
```

#### Rate Limiting & DoS Protection

```python
# Redis-based rate limiting
class RateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    async def check_rate_limit(self, key: str, limit: int, window: int) -> bool:
        """
        Args:
            key: Rate limit key (user_id, IP, etc.)
            limit: Maximum requests allowed
            window: Time window in seconds
        """
        current_time = int(time.time())
        pipeline = self.redis.pipeline()
        
        # Sliding window log approach
        pipeline.zremrangebyscore(key, 0, current_time - window)
        pipeline.zadd(key, {str(current_time): current_time})
        pipeline.zcard(key)
        pipeline.expire(key, window)
        
        results = await pipeline.execute()
        request_count = results[2]
        
        return request_count <= limit

# Rate limit decorator
def rate_limit(requests_per_minute: int = 60):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get('request') or args[0]
            user_id = getattr(request.state, 'user_id', None)
            client_ip = request.client.host
            
            # Multiple rate limit checks
            checks = [
                f"user:{user_id}",  # Per-user limit
                f"ip:{client_ip}",  # Per-IP limit
                f"global"           # Global limit
            ]
            
            for check_key in checks:
                if not await rate_limiter.check_rate_limit(
                    check_key, requests_per_minute, 60
                ):
                    raise HTTPException(429, "Rate limit exceeded")
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator
```

## Integration Architecture

### Third-Party Integration Framework

```
┌─────────────────────────────────────────────────┐
│              Integration Gateway                │
│  • Authentication & rate limiting              │
│  • Request/response transformation              │
│  • Error handling & retry logic                │
├─────────────────────────────────────────────────┤
│               Integration Services              │
├─────────────────┬───────────────┬───────────────┤
│   SSO/Identity  │   Project     │   Business    │
│   Management    │   Management  │   Systems     │
│                 │               │               │
│ • Azure AD      │ • Jira        │ • SAP         │
│ • Okta          │ • GitHub      │ • Oracle      │
│ • Google        │ • Asana       │ • Salesforce  │
│ • SAML 2.0      │ • Monday.com  │ • Workday     │
├─────────────────┼───────────────┼───────────────┤
│  Communication  │   File        │   Analytics   │
│  & Alerts       │   Storage     │   & BI        │
│                 │               │               │
│ • Slack         │ • OneDrive    │ • Tableau     │
│ • Teams         │ • Google Drive│ • Power BI    │
│ • Email (SMTP)  │ • Dropbox     │ • Looker      │
│ • SMS (Twilio)  │ • Box         │ • Qlik        │
└─────────────────┴───────────────┴───────────────┘
```

### Integration Patterns

#### 1. **Webhook-Based Integrations**

```python
# Outbound webhook system
class WebhookDelivery:
    async def send_webhook(self, event: Event, webhook_config: WebhookConfig):
        payload = {
            "event_type": event.type,
            "tenant_id": event.tenant_id,
            "timestamp": event.timestamp.isoformat(),
            "data": event.data,
            "signature": self.generate_signature(event.data, webhook_config.secret)
        }
        
        retry_config = ExponentialBackoff(
            initial_delay=1,
            max_delay=300, 
            max_retries=5
        )
        
        for attempt in range(retry_config.max_retries):
            try:
                async with httpx.AsyncClient(timeout=30) as client:
                    response = await client.post(
                        webhook_config.url,
                        json=payload,
                        headers={
                            "X-AtlasPM-Signature": payload["signature"],
                            "X-AtlasPM-Event": event.type,
                            "Content-Type": "application/json"
                        }
                    )
                    
                if response.status_code == 200:
                    await self.log_delivery_success(webhook_config.id, event.id)
                    return
                    
            except Exception as e:
                await self.log_delivery_error(webhook_config.id, event.id, str(e))
                await asyncio.sleep(retry_config.get_delay(attempt))
        
        # Mark as failed after all retries
        await self.mark_delivery_failed(webhook_config.id, event.id)
```

#### 2. **API-Based Sync Integrations**

```python
# Jira integration for project sync
class JiraIntegration:
    def __init__(self, config: JiraConfig):
        self.base_url = config.base_url
        self.auth = HTTPBasicAuth(config.username, config.api_token)
        
    async def sync_project_to_jira(self, project: Project):
        """Sync AtlasPM project to Jira as epic"""
        
        jira_payload = {
            "fields": {
                "project": {"key": project.external_config.get("jira_project_key")},
                "summary": project.name,
                "description": project.description,
                "issuetype": {"name": "Epic"},
                "customfield_10011": project.code,  # Epic Name
                "labels": ["atlaspm", f"portfolio-{project.portfolio_id}"]
            }
        }
        
        if project.external_id:
            # Update existing
            url = f"{self.base_url}/rest/api/3/issue/{project.external_id}"
            method = "PUT"
        else:
            # Create new
            url = f"{self.base_url}/rest/api/3/issue"
            method = "POST"
            
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method, url, 
                json=jira_payload, 
                auth=self.auth
            )
            
        if response.status_code in [200, 201]:
            if not project.external_id:
                project.external_id = response.json()["key"]
                await self.update_project_external_id(project)
```

#### 3. **File Sync Integrations**

```python
# OneDrive integration for document sync
class OneDriveIntegration:
    async def sync_attachments(self, project_id: str):
        """Sync project attachments with OneDrive folder"""
        
        # Get project attachments
        attachments = await get_project_attachments(project_id)
        
        # Create/get OneDrive folder
        folder_path = f"/AtlasPM/Projects/{project_id}"
        folder = await self.ensure_folder_exists(folder_path)
        
        for attachment in attachments:
            if not attachment.external_sync_id:
                # Upload new file
                file_content = await get_attachment_content(attachment.id)
                uploaded_file = await self.upload_file(
                    folder["id"], 
                    attachment.filename,
                    file_content
                )
                
                # Update attachment with OneDrive file ID
                await update_attachment_external_id(
                    attachment.id, 
                    uploaded_file["id"]
                )
```

### API Rate Limiting & Quotas

```python
# Integration-specific rate limiting
class IntegrationRateLimiter:
    LIMITS = {
        "jira": {"requests_per_minute": 100, "daily_quota": 10000},
        "slack": {"requests_per_minute": 60, "daily_quota": 50000},
        "onedrive": {"requests_per_minute": 120, "daily_quota": 100000}
    }
    
    async def check_integration_quota(self, integration_type: str, tenant_id: str):
        daily_key = f"quota:{integration_type}:{tenant_id}:{date.today()}"
        minute_key = f"rate:{integration_type}:{tenant_id}:{int(time.time() / 60)}"
        
        limits = self.LIMITS[integration_type]
        
        # Check daily quota
        daily_usage = await redis.get(daily_key) or 0
        if int(daily_usage) >= limits["daily_quota"]:
            raise QuotaExceededError(f"Daily quota exceeded for {integration_type}")
        
        # Check per-minute rate
        minute_usage = await redis.get(minute_key) or 0
        if int(minute_usage) >= limits["requests_per_minute"]:
            raise RateLimitError(f"Rate limit exceeded for {integration_type}")
        
        # Increment counters
        await redis.incr(daily_key)
        await redis.incr(minute_key)
        await redis.expire(minute_key, 60)
```

## Monitoring & Observability

### Application Performance Monitoring (APM)

```
┌─────────────────────────────────────────────────┐
│                  Monitoring Stack               │
├─────────────────────────────────────────────────┤
│  Metrics Collection                             │
│  • Prometheus (system & custom metrics)        │
│  • StatsD (application metrics)                │
│  • OpenTelemetry (distributed tracing)         │
├─────────────────────────────────────────────────┤
│  Log Aggregation                                │
│  • Structured JSON logging                     │
│  • ELK Stack (Elasticsearch/Logstash/Kibana)   │
│  • Log retention policies                       │
├─────────────────────────────────────────────────┤
│  Alerting & Notification                        │
│  • PagerDuty integration                        │
│  • Slack alerts for dev team                   │
│  • SMS/email for critical issues               │
├─────────────────────────────────────────────────┤
│  Dashboards & Visualization                     │
│  • Grafana operational dashboards              │
│  • Business metrics dashboards                 │
│  • Real-time system health                     │
└─────────────────────────────────────────────────┘
```

### Key Metrics & Alerts

#### Application Metrics

```python
# Custom metrics collection
from prometheus_client import Counter, Histogram, Gauge

# Business metrics
projects_created = Counter('projects_created_total', 'Total projects created', ['tenant_id'])
tasks_completed = Counter('tasks_completed_total', 'Total tasks completed', ['tenant_id', 'project_type'])
user_sessions = Gauge('active_user_sessions', 'Active user sessions', ['tenant_id'])

# Performance metrics  
api_request_duration = Histogram(
    'api_request_duration_seconds',
    'API request duration',
    ['method', 'endpoint', 'status_code']
)

database_query_duration = Histogram(
    'database_query_duration_seconds', 
    'Database query duration',
    ['collection', 'operation']
)

# Error metrics
api_errors = Counter('api_errors_total', 'API errors', ['endpoint', 'error_type'])
integration_failures = Counter(
    'integration_failures_total',
    'Integration failures', 
    ['integration_type', 'error_reason']
)
```

#### Alert Rules Configuration

```yaml
# Prometheus alert rules
groups:
  - name: atlaspm_alerts
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: rate(api_errors_total[5m]) > 0.1
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} errors/second"
      
      # Database performance  
      - alert: SlowDatabaseQueries
        expr: histogram_quantile(0.95, database_query_duration_seconds) > 1.0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Database queries are slow"
          description: "95th percentile query time: {{ $value }}s"
      
      # Memory usage
      - alert: HighMemoryUsage
        expr: process_resident_memory_bytes / 1024 / 1024 / 1024 > 3.5
        for: 3m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage"
          description: "Memory usage: {{ $value }}GB"
      
      # Integration failures
      - alert: IntegrationDown
        expr: increase(integration_failures_total[10m]) > 5
        for: 0m
        labels:
          severity: critical
        annotations:
          summary: "Integration experiencing failures"
          description: "{{ $labels.integration_type }} failing"
```

### Distributed Tracing

```python
# OpenTelemetry instrumentation
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.pymongo import PymongoInstrumentor

# Initialize tracing
tracer = trace.get_tracer(__name__)

# Automatic instrumentation
FastAPIInstrumentor.instrument_app(app)
PymongoInstrumentor().instrument()

# Custom spans for business logic
@tracer.start_as_current_span("project_creation")
async def create_project(project_data: ProjectCreate, user_context: UserContext):
    span = trace.get_current_span()
    span.set_attribute("tenant_id", user_context.tenant_id)
    span.set_attribute("user_id", user_context.user_id)
    span.set_attribute("project_type", project_data.project_type)
    
    try:
        # Business logic with nested spans
        with tracer.start_as_current_span("validate_project_data"):
            await validate_project_creation(project_data, user_context)
        
        with tracer.start_as_current_span("save_to_database"):
            project = await save_project(project_data)
        
        with tracer.start_as_current_span("send_notifications"):
            await notify_stakeholders(project)
        
        span.set_attribute("project_id", project.id)
        span.set_status(trace.Status(trace.StatusCode.OK))
        
        return project
        
    except Exception as e:
        span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
        span.record_exception(e)
        raise
```

### Business Intelligence Dashboards

#### Executive Dashboard Metrics

```sql
-- Key performance indicators for executive reporting
SELECT 
    tenant_name,
    DATE_TRUNC('month', created_at) as month,
    COUNT(*) as projects_created,
    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as projects_completed,
    AVG(percent_complete) as avg_progress,
    SUM(financials.total_budget) as total_budget,
    SUM(financials.spent_amount) as total_spent,
    COUNT(DISTINCT project_manager_id) as active_managers
FROM projects 
JOIN tenants ON projects.tenant_id = tenants.id
WHERE created_at >= NOW() - INTERVAL '12 months'
GROUP BY tenant_name, month
ORDER BY tenant_name, month;
```

#### Operational Health Dashboard

```python
# Real-time system health metrics
async def get_system_health():
    return {
        "api": {
            "status": await check_api_health(),
            "response_time_p95": await get_response_time_percentile(95),
            "error_rate_5m": await get_error_rate(minutes=5)
        },
        "database": {
            "status": await check_mongodb_health(),
            "connections": await get_active_connections(),
            "query_time_avg": await get_avg_query_time()
        },
        "cache": {
            "status": await check_redis_health(),
            "hit_rate": await get_cache_hit_rate(),
            "memory_usage": await get_redis_memory_usage()
        },
        "integrations": {
            integration_type: await check_integration_health(integration_type)
            for integration_type in ["jira", "slack", "onedrive"]
        }
    }
```

## Deployment Architecture

### Container Orchestration (Kubernetes)

```yaml
# Kubernetes deployment configuration
apiVersion: apps/v1
kind: Deployment
metadata:
  name: atlaspm-api
  labels:
    app: atlaspm-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: atlaspm-api
  template:
    metadata:
      labels:
        app: atlaspm-api
    spec:
      containers:
      - name: atlaspm-api
        image: atlaspm/api:v1.0.0
        ports:
        - containerPort: 8001
        env:
        - name: MONGO_URL
          valueFrom:
            secretKeyRef:
              name: atlaspm-secrets
              key: mongo-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: atlaspm-secrets
              key: redis-url
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi" 
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8001
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8001
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: atlaspm-api-service
spec:
  selector:
    app: atlaspm-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8001
  type: ClusterIP
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: atlaspm-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - api.atlaspm.com
    secretName: atlaspm-tls
  rules:
  - host: api.atlaspm.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: atlaspm-api-service
            port:
              number: 80
```

### CI/CD Pipeline

```yaml
# GitHub Actions workflow
name: AtlasPM CI/CD
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      mongodb:
        image: mongo:5.0
        options: >-
          --health-cmd "echo 'db.runCommand({ping: 1})' | mongo"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:6-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Run tests
      run: |
        pytest tests/ --cov=app --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
    
  security-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Run security scan
      uses: securecodewarrior/github-action-add-sarif@v1
      with:
        sarif-file: security-scan-results.sarif
    
    - name: Dependency vulnerability scan
      run: |
        pip install safety
        safety check -r requirements.txt
  
  build-and-deploy:
    needs: [test, security-scan]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: |
        docker build -t atlaspm/api:${{ github.sha }} .
        docker tag atlaspm/api:${{ github.sha }} atlaspm/api:latest
    
    - name: Push to registry
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker push atlaspm/api:${{ github.sha }}
        docker push atlaspm/api:latest
    
    - name: Deploy to staging
      run: |
        kubectl set image deployment/atlaspm-api atlaspm-api=atlaspm/api:${{ github.sha }} -n staging
        kubectl rollout status deployment/atlaspm-api -n staging
    
    - name: Run integration tests
      run: |
        pytest integration-tests/ --staging-url=${{ secrets.STAGING_URL }}
    
    - name: Deploy to production
      if: success()
      run: |
        kubectl set image deployment/atlaspm-api atlaspm-api=atlaspm/api:${{ github.sha }} -n production
        kubectl rollout status deployment/atlaspm-api -n production
```

### Infrastructure as Code

```terraform
# Terraform configuration for AWS deployment
provider "aws" {
  region = var.aws_region
}

# EKS Cluster
module "eks" {
  source = "terraform-aws-modules/eks/aws"
  
  cluster_name    = "atlaspm-${var.environment}"
  cluster_version = "1.24"
  
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets
  
  node_groups = {
    main = {
      desired_capacity = var.node_group_desired_capacity
      max_capacity     = var.node_group_max_capacity
      min_capacity     = var.node_group_min_capacity
      
      instance_types = ["t3.large", "t3.xlarge"]
      
      k8s_labels = {
        Environment = var.environment
        Application = "atlaspm"
      }
    }
  }
}

# MongoDB Atlas Cluster
resource "mongodbatlas_cluster" "atlaspm" {
  project_id   = var.mongodb_atlas_project_id
  name         = "atlaspm-${var.environment}"
  
  cluster_type = "REPLICASET"
  
  replication_specs {
    num_shards = 1
    regions_config {
      region_name     = var.mongodb_region
      electable_nodes = 3
      priority        = 7
      read_only_nodes = 0
    }
  }
  
  provider_backup_enabled      = true
  auto_scaling_disk_gb_enabled = true
  
  provider_instance_size_name = var.mongodb_instance_size
}

# ElastiCache Redis
resource "aws_elasticache_replication_group" "atlaspm" {
  replication_group_id         = "atlaspm-${var.environment}"
  description                  = "AtlasPM Redis cluster"
  
  num_cache_clusters           = 2
  node_type                    = var.redis_node_type
  port                         = 6379
  parameter_group_name         = "default.redis6.x"
  
  subnet_group_name            = aws_elasticache_subnet_group.atlaspm.name
  security_group_ids           = [aws_security_group.redis.id]
  
  at_rest_encryption_enabled   = true
  transit_encryption_enabled   = true
  
  automatic_failover_enabled   = true
  multi_az_enabled            = true
  
  apply_immediately           = true
}

# Application Load Balancer
resource "aws_lb" "atlaspm" {
  name               = "atlaspm-${var.environment}"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets           = module.vpc.public_subnets
  
  enable_deletion_protection = var.environment == "production"
  
  access_logs {
    bucket  = aws_s3_bucket.alb_logs.bucket
    prefix  = "atlaspm-alb"
    enabled = true
  }
}
```

This comprehensive architecture specification provides the foundation for building and scaling AtlasPM as an enterprise-grade portfolio and project management platform. The architecture emphasizes security, scalability, multi-tenancy, and comprehensive integration capabilities while maintaining high performance and reliability standards.
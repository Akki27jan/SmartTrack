# SmartTrack API — Project Structure

This document explains the modular file structure of the SmartTrack backend API, what each folder and file does, and how to add new features.

---

## Directory Overview

```
backend-api/
├── main.py                  # App entry point — wires everything together
├── database.py              # Database engine, session, and Base
├── models/                  # SQLAlchemy table definitions (DB layer)
│   ├── __init__.py          # Re-exports all models
│   ├── company.py           # CompanyDB
│   ├── employee.py          # EmployeeDB
│   ├── hr.py                # CompanyHRDB
│   ├── notification.py      # EmployeeNotificationDB, CompanyNotificationDB
│   ├── audit.py             # AuditLogDB
│   └── dispute.py           # EmployeeDisputeDB, DisputeResponseDB, EvidenceDB
├── schemas/                 # Pydantic models (request/response validation)
│   ├── __init__.py          # Re-exports all schemas
│   ├── company.py           # Company, CompanySignup, CompanyLogin
│   ├── employee.py          # Employee, EmployeeSignup, EmployeeLogin
│   ├── hr.py                # CompanyHR, HRSignup, HRLogin
│   ├── notification.py      # EmployeeNotification, CompanyNotification
│   ├── audit.py             # AuditLog
│   └── dispute.py           # EmployeeDispute, DisputeResponse, Evidence, ResolveDispute
├── routes/                  # API route handlers (business logic)
│   ├── __init__.py          # Re-exports all routers
│   ├── company.py           # /company/signup, /company/login
│   ├── employee.py          # /employee/signup, /employee/login
│   ├── hr.py                # /hr/signup, /hr/login
│   ├── notification.py      # notification endpoints
│   ├── audit.py             # audit log endpoints
│   └── dispute.py           # dispute, response, evidence endpoints
├── utils/                   # Shared helper functions
│   ├── __init__.py
│   └── id_generator.py      # All ID generation functions
├── test_endpoints.py        # Smoke test script for all endpoints
├── docker-compose.yaml      # PostgreSQL container config
├── .env                     # Environment variables (DATABASE_URL)
└── guide.md                 # Original project guide
```

---

## What Each Layer Does

### `main.py` — The Entry Point

This is the only file `uvicorn` loads. It does 3 things:

1. **Imports all models** so SQLAlchemy registers them with `Base.metadata`
2. **Creates all DB tables** via `Base.metadata.create_all()`
3. **Registers all routers** via `app.include_router()`

> You should almost never need to add business logic here. Just import and register new routers.

---

### `database.py` — Database Configuration

Contains the core database setup:

| Object | Purpose |
|--------|---------|
| `engine` | SQLAlchemy engine connected to PostgreSQL |
| `Base` | Declarative base that all models inherit from |
| `SessionLocal` | Session factory for creating DB sessions |
| `get_db()` | FastAPI dependency that provides a DB session per request |

> This file has **no models** in it. Models live in `models/`.

---

### `models/` — Database Table Definitions

Each file defines one or more SQLAlchemy ORM classes that map to PostgreSQL tables.

| File | Class(es) | DB Table(s) |
|------|-----------|-------------|
| `company.py` | `CompanyDB` | `companies` |
| `employee.py` | `EmployeeDB` | `employees` |
| `hr.py` | `CompanyHRDB` | `company_hr` |
| `notification.py` | `EmployeeNotificationDB`, `CompanyNotificationDB` | `employee_notifications`, `company_notifications` |
| `audit.py` | `AuditLogDB` | `audit_logs` |
| `dispute.py` | `EmployeeDisputeDB`, `DisputeResponseDB`, `EvidenceDB` | `employees_disputes`, `dispute_response`, `evidence` |

**Every model must:**
- Import `Base` from `database.py`
- Inherit from `Base`
- Be imported in `models/__init__.py` so it gets registered

---

### `schemas/` — Request/Response Validation

Each file defines Pydantic `BaseModel` classes that validate incoming JSON request bodies.

| File | Schema(s) | Used For |
|------|-----------|----------|
| `company.py` | `Company`, `CompanySignup`, `CompanyLogin` | Company CRUD |
| `employee.py` | `Employee`, `EmployeeSignup`, `EmployeeLogin` | Employee CRUD |
| `hr.py` | `CompanyHR`, `HRSignup`, `HRLogin` | HR CRUD |
| `notification.py` | `EmployeeNotification`, `CompanyNotification` | Sending notifications |
| `audit.py` | `AuditLog` | Creating audit entries |
| `dispute.py` | `EmployeeDispute`, `DisputeResponse`, `Evidence`, `ResolveDispute` | Dispute system |

**Naming convention:**
- `XxxSignup` — fields needed for registration (no ID, server generates it)
- `XxxLogin` — fields needed for authentication
- `Xxx` — full model with all fields including ID

---

### `routes/` — API Endpoints

Each file creates an `APIRouter()` and defines route handler functions. This is where the business logic lives.

| File | Endpoints |
|------|-----------|
| `company.py` | `POST /company/signup`, `POST /company/login` |
| `employee.py` | `POST /employee/signup`, `POST /employee/login` |
| `hr.py` | `POST /hr/signup`, `POST /hr/login` |
| `notification.py` | `POST /employee/notification`, `POST /company/notification`, `GET /employee/{id}/notifications`, `GET /company/{id}/notifications` |
| `audit.py` | `POST /audit-log`, `GET /audit-logs/hr/{id}`, `GET /audit-logs/employee/{id}` |
| `dispute.py` | `POST /employee/dispute`, `GET /employee/{id}/disputes`, `GET /company/{id}/disputes`, `POST /dispute/response`, `POST /dispute/evidence`, `PUT /dispute/{id}/resolve` |

**Every route file:**
- Creates `router = APIRouter()`
- Imports its schemas from `schemas/`
- Imports its models from `models/`
- Imports helpers from `utils/`

---

### `utils/` — Shared Helpers

| File | Functions |
|------|-----------|
| `id_generator.py` | `generate_custom_id()` — AAT000 format for companies/employees/HR |
| | `generate_audit_log_id()` — AUD000 format |
| | `generate_dispute_id()` — DIS000 format |
| | `generate_response_id()` — RES000 format |
| | `generate_evidence_id()` — EVD000 format |

---

## How Data Flows Through the App

```
Client Request
      │
      ▼
  main.py (FastAPI app)
      │
      ▼
  routes/xxx.py (APIRouter handles the request)
      │
      ├──▶ schemas/xxx.py (validates the request body)
      │
      ├──▶ utils/id_generator.py (generates IDs if needed)
      │
      ├──▶ models/xxx.py (ORM class for DB operations)
      │
      └──▶ database.py (get_db provides the session)
      │
      ▼
  JSON Response
```

---

## How to Add a New Feature

For example, adding a **"Leave Request"** feature:

### Step 1: Create the model
```python
# models/leave.py
from sqlalchemy import Column, String, DateTime, ForeignKey
from datetime import datetime
from database import Base

class LeaveRequestDB(Base):
    __tablename__ = "leave_requests"
    Leave_ID = Column(String, primary_key=True)
    Employee_ID = Column(String, ForeignKey("employees.Employee_ID"), nullable=False)
    Reason = Column(String, nullable=False)
    Status = Column(String, default="Pending")
    Created_At = Column(DateTime, default=datetime.utcnow)
```

### Step 2: Create the schema
```python
# schemas/leave.py
from pydantic import BaseModel

class LeaveRequest(BaseModel):
    Employee_ID: str
    Reason: str
```

### Step 3: Add the ID generator
```python
# In utils/id_generator.py, add:
def generate_leave_id(db: Session) -> str:
    from models.leave import LeaveRequestDB
    count = db.query(LeaveRequestDB).count()
    return f"LEV{str(count + 1).zfill(3)}"
```

### Step 4: Create the route
```python
# routes/leave.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.leave import LeaveRequestDB
from schemas.leave import LeaveRequest
from utils.id_generator import generate_leave_id

router = APIRouter()

@router.post("/employee/leave")
def request_leave(data: LeaveRequest, db: Session = Depends(get_db)):
    leave_id = generate_leave_id(db)
    leave = LeaveRequestDB(Leave_ID=leave_id, Employee_ID=data.Employee_ID, Reason=data.Reason)
    db.add(leave)
    db.commit()
    db.refresh(leave)
    return {"message": "Leave requested", "Leave_ID": leave_id}
```

### Step 5: Register everything

Add to each `__init__.py`:
```python
# models/__init__.py
from models.leave import LeaveRequestDB

# schemas/__init__.py
from schemas.leave import LeaveRequest

# routes/__init__.py
from routes.leave import router as leave_router
```

Add to `main.py`:
```python
from models import LeaveRequestDB          # noqa: F401
from routes.leave import router as leave_router
app.include_router(leave_router)
```

**Done!** The server auto-reloads and your new endpoint is live.

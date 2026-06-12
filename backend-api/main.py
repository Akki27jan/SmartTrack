from fastapi import FastAPI
from database import engine, Base

# Import all models so they register with Base.metadata
from models import CompanyDB, EmployeeDB, CompanyHRDB, EmployeeNotificationDB, CompanyNotificationDB, AuditLogDB  # noqa: F401
from models import EmployeeDisputeDB, DisputeResponseDB, EvidenceDB  # noqa: F401
from models import EmployeeRecordDB  # noqa: F401

# Import routers
from routes.company import router as company_router
from routes.employee import router as employee_router
from routes.hr import router as hr_router
from routes.notification import router as notification_router
from routes.audit import router as audit_router
from routes.dispute import router as dispute_router
from routes.employee_record import router as employee_record_router

app = FastAPI()

# ---------- Create all tables ----------
Base.metadata.create_all(bind=engine)

# ---------- Register routers ----------
app.include_router(company_router)
app.include_router(employee_router)
app.include_router(hr_router)
app.include_router(notification_router)
app.include_router(audit_router)
app.include_router(dispute_router)
app.include_router(employee_record_router)

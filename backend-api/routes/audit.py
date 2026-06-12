from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.hr import CompanyHRDB
from models.employee import EmployeeDB
from models.audit import AuditLogDB
from schemas.audit import AuditLog
from utils.id_generator import generate_audit_log_id

router = APIRouter()


@router.post("/audit-log")
def create_audit_log(data: AuditLog, db: Session = Depends(get_db)):
    hr = db.query(CompanyHRDB).filter(CompanyHRDB.HR_ID == data.HR_ID).first()
    if not hr:
        raise HTTPException(status_code=404, detail="HR not found")

    employee = db.query(EmployeeDB).filter(EmployeeDB.Employee_ID == data.Employee_ID).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    log_id = generate_audit_log_id(db)

    new_log = AuditLogDB(
        Audit_Log_ID=log_id,
        HR_ID=data.HR_ID,
        Action_Type=data.Action_Type,
        Employee_ID=data.Employee_ID
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return {"message": "Audit log created", "Audit_Log_ID": log_id}


@router.get("/audit-logs/hr/{hr_id}")
def get_audit_logs_by_hr(hr_id: str, db: Session = Depends(get_db)):
    logs = db.query(AuditLogDB).filter(AuditLogDB.HR_ID == hr_id).all()
    return logs


@router.get("/audit-logs/employee/{employee_id}")
def get_audit_logs_by_employee(employee_id: str, db: Session = Depends(get_db)):
    logs = db.query(AuditLogDB).filter(AuditLogDB.Employee_ID == employee_id).all()
    return logs

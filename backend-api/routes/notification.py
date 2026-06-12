from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.employee import EmployeeDB
from models.company import CompanyDB
from models.notification import EmployeeNotificationDB, CompanyNotificationDB
from schemas.notification import EmployeeNotification, CompanyNotification

router = APIRouter()


@router.post("/employee/notification")
def send_employee_notification(data: EmployeeNotification, db: Session = Depends(get_db)):
    employee = db.query(EmployeeDB).filter(EmployeeDB.Employee_ID == data.Employee_ID).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    notification = EmployeeNotificationDB(
        Employee_ID=data.Employee_ID,
        Type=data.Type,
        Subject=data.Subject,
        Message=data.Message,
        Status=True
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return {
        "message": "Notification sent to employee",
        "notification_id": notification.Notif_ID
    }


@router.post("/company/notification")
def send_company_notification(data: CompanyNotification, db: Session = Depends(get_db)):
    company = db.query(CompanyDB).filter(CompanyDB.Company_ID == data.Company_ID).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    notification = CompanyNotificationDB(
        Company_ID=data.Company_ID,
        Type=data.Type,
        Subject=data.Subject,
        Message=data.Message,
        Status="sent"
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return {
        "message": "Notification sent to company",
        "notification_id": notification.Notif_ID
    }


@router.get("/employee/{employee_id}/notifications")
def get_employee_notifications(employee_id: str, db: Session = Depends(get_db)):
    notifications = db.query(EmployeeNotificationDB).filter(
        EmployeeNotificationDB.Employee_ID == employee_id
    ).all()

    return notifications


@router.get("/company/{company_id}/notifications")
def get_company_notifications(company_id: str, db: Session = Depends(get_db)):
    notifications = db.query(CompanyNotificationDB).filter(
        CompanyNotificationDB.Company_ID == company_id
    ).all()

    return notifications

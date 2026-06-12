from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from datetime import datetime
from database import Base


class EmployeeNotificationDB(Base):
    __tablename__ = "employee_notifications"

    Notif_ID = Column(Integer, primary_key=True, index=True)
    Employee_ID = Column(String, ForeignKey("employees.Employee_ID"), nullable=False)
    Type = Column(String)
    Subject = Column(String)
    Message = Column(String)
    Status = Column(Boolean, default=True)
    Sent_Time = Column(DateTime, default=datetime.utcnow)


class CompanyNotificationDB(Base):
    __tablename__ = "company_notifications"

    Notif_ID = Column(Integer, primary_key=True, index=True)
    Company_ID = Column(String, ForeignKey("companies.Company_ID"), nullable=False)
    Type = Column(String)
    Subject = Column(String)
    Message = Column(String)
    Status = Column(String, default="sent")
    Sent_Time = Column(DateTime, default=datetime.utcnow)

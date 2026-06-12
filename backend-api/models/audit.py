from sqlalchemy import Column, String, DateTime, ForeignKey
from datetime import datetime
from database import Base


class AuditLogDB(Base):
    __tablename__ = "audit_logs"

    Audit_Log_ID = Column(String, primary_key=True)
    Created_At = Column(DateTime, default=datetime.utcnow)
    HR_ID = Column(String, ForeignKey("company_hr.HR_ID"), nullable=False)
    Action_Type = Column(String, nullable=False)
    Employee_ID = Column(String, ForeignKey("employees.Employee_ID"), nullable=False)

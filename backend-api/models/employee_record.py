from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric
from datetime import datetime
from database import Base


class EmployeeRecordDB(Base):
    __tablename__ = "employee_records"

    Record_ID = Column(String, primary_key=True)
    Employee_ID = Column(String, ForeignKey("employees.Employee_ID"), nullable=False)
    Company_ID = Column(String, ForeignKey("companies.Company_ID"), nullable=False)
    Department = Column(String, nullable=False)
    Designation = Column(String, nullable=False)
    Joining_Date = Column(DateTime, nullable=False)
    Leaving_Date = Column(DateTime, nullable=True)
    Reason_of_Exit = Column(String, nullable=True)
    Rating = Column(Numeric(precision=3, scale=1), nullable=False)
    Conduct_Flags = Column(String, nullable=True)
    Would_Hire = Column(String, nullable=False)
    Created_At = Column(DateTime, default=datetime.utcnow)
    Last_Updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    Additional_Notes = Column(String, nullable=True)

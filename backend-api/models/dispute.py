from sqlalchemy import Column, String, DateTime, ForeignKey
from datetime import datetime
from database import Base


class EmployeeDisputeDB(Base):
    __tablename__ = "employees_disputes"

    Dispute_ID = Column(String, primary_key=True)
    Raised_By = Column(String, ForeignKey("employees.Employee_ID"), nullable=False)
    Raised_Against = Column(String, ForeignKey("companies.Company_ID"), nullable=False)
    Dispute_Type = Column(String, nullable=False)
    Description = Column(String, nullable=False)
    Status = Column(String, default="Open")
    Submission_Time = Column(DateTime, default=datetime.utcnow)
    Resolve_Time = Column(DateTime, nullable=True)


class DisputeResponseDB(Base):
    __tablename__ = "dispute_response"

    Response_ID = Column(String, primary_key=True)
    Dispute_ID = Column(String, ForeignKey("employees_disputes.Dispute_ID"), nullable=False)
    Time_Raised = Column(DateTime, default=datetime.utcnow)
    Resolve_Time = Column(DateTime, nullable=True)


class EvidenceDB(Base):
    __tablename__ = "evidence"

    Evidence_ID = Column(String, primary_key=True)
    Response_ID = Column(String, ForeignKey("dispute_response.Response_ID"), nullable=True)
    Dispute_ID = Column(String, ForeignKey("employees_disputes.Dispute_ID"), nullable=False)
    File_Url = Column(String, nullable=False)
    Upload_Time = Column(DateTime, default=datetime.utcnow)
    Uploaded_By = Column(String, nullable=False)

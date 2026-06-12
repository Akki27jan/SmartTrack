import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, String, ForeignKey, Integer, Boolean, DateTime, Numeric
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# ---------- SQLAlchemy Table Models ----------

class CompanyDB(Base):
    __tablename__ = "companies"

    Company_ID = Column(String, primary_key=True)
    Name = Column(String, nullable=False)
    Gstin = Column(String, unique=True, nullable=False)
    Address = Column(String)
    Password = Column(String, nullable=False)
    Domain = Column(String)


class EmployeeDB(Base):
    __tablename__ = "employees"

    Employee_ID = Column(String, primary_key=True)
    Name = Column(String, nullable=False)
    Email = Column(String, unique=True, nullable=False)
    Password = Column(String, nullable=False)


class CompanyHRDB(Base):
    __tablename__ = "company_hr"

    HR_ID = Column(String, primary_key=True)
    Company_ID = Column(String, ForeignKey("companies.Company_ID"), nullable=False)
    Name = Column(String, nullable=False)
    Company_Email = Column(String, unique=True, nullable=False)
    Password = Column(String, nullable=False)

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

class AuditLogDB(Base):
    __tablename__ = "audit_logs"

    Audit_Log_ID = Column(String, primary_key=True)
    Created_At = Column(DateTime, default=datetime.utcnow)
    HR_ID = Column(String, ForeignKey("company_hr.HR_ID"), nullable=False)
    Action_Type = Column(String, nullable=False)
    Employee_ID = Column(String, ForeignKey("employees.Employee_ID"), nullable=False)

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


class PlanDB(Base):
    __tablename__ = "plans"

    Plan_ID = Column(String, primary_key=True)
    Tier = Column(String, nullable=False)
    Pricing = Column(Numeric(10, 2), default=0)
    Tax = Column(Numeric(10, 2), default=0)
    Records = Column(Integer, default=0)
    Searches = Column(Integer, default=0)
    Total_Amount = Column(Numeric(10, 2), default=0)


class AddonPricingDB(Base):
    __tablename__ = "addons_pricing"

    Addon_ID = Column(String, primary_key=True)
    Type = Column(String)
    Quantity = Column(Integer)
    Price = Column(Numeric(10, 2))
    Tax = Column(Numeric(10, 2))


class BillingDetailsDB(Base):
    __tablename__ = "billing_details"

    Billing_ID = Column(String, primary_key=True)
    Company_ID = Column(String, ForeignKey("companies.Company_ID"), nullable=False)


class CompanySubscriptionDB(Base):
    __tablename__ = "company_subscriptions"

    Subscription_ID = Column(String, primary_key=True)
    Company_ID = Column(String, ForeignKey("companies.Company_ID"), nullable=False)
    Plan_ID = Column(String, ForeignKey("plans.Plan_ID"), nullable=False)
    Start_Date = Column(DateTime, default=datetime.utcnow)
    End_Date = Column(DateTime)
    Records_Used = Column(Integer, default=0)
    Searches_Used = Column(Integer, default=0)
    Billing_ID = Column(String, ForeignKey("billing_details.Billing_ID"), nullable=True)


class AddonPurchaseDB(Base):
    __tablename__ = "addon_purchase"

    Addon_Purchase_ID = Column(String, primary_key=True)
    Addon_ID = Column(String, ForeignKey("addons_pricing.Addon_ID"), nullable=False)
    Quantity = Column(Integer)
    Billing_ID = Column(String, ForeignKey("billing_details.Billing_ID"), nullable=True)
    Subscription_ID = Column(String, ForeignKey("company_subscriptions.Subscription_ID"), nullable=False)
    Date_Time = Column(DateTime, default=datetime.utcnow)


class AddonInvoiceDB(Base):
    __tablename__ = "addon_invoice"

    Addon_Invoice_ID = Column(String, primary_key=True)
    Company_ID = Column(String, ForeignKey("companies.Company_ID"), nullable=False)
    Billing_ID = Column(String, ForeignKey("billing_details.Billing_ID"), nullable=True)
    File_URL = Column(String)
    Date = Column(DateTime, default=datetime.utcnow)
    Addon_Purchase_ID = Column(String, ForeignKey("addon_purchase.Addon_Purchase_ID"), nullable=False)
    Price = Column(Numeric(10, 2))
    Tax = Column(Numeric(10, 2))
    Total_Price = Column(Numeric(10, 2))
    Date_Time = Column(DateTime, default=datetime.utcnow)


class SubscriptionInvoiceDB(Base):
    __tablename__ = "subscription_invoice"

    Subscription_Invoice_ID = Column(String, primary_key=True)
    Company_ID = Column(String, ForeignKey("companies.Company_ID"), nullable=False)
    Billing_ID = Column(String, ForeignKey("billing_details.Billing_ID"), nullable=True)
    File_URL = Column(String)
    Date = Column(DateTime, default=datetime.utcnow)
    Subscription_ID = Column(String, ForeignKey("company_subscriptions.Subscription_ID"), nullable=False)
    Price = Column(Numeric(10, 2))
    Tax = Column(Numeric(10, 2))
    Total_Price = Column(Numeric(10, 2))
    Date_Time = Column(DateTime, default=datetime.utcnow)
# ---------- Create all tables ----------

Base.metadata.create_all(bind=engine)


# ---------- DB session dependency ----------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

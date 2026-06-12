from sqlalchemy import Column, String, ForeignKey
from database import Base


class CompanyHRDB(Base):
    __tablename__ = "company_hr"

    HR_ID = Column(String, primary_key=True)
    Company_ID = Column(String, ForeignKey("companies.Company_ID"), nullable=False)
    Name = Column(String, nullable=False)
    Company_Email = Column(String, unique=True, nullable=False)
    Password = Column(String, nullable=False)

from sqlalchemy import Column, String
from database import Base


class CompanyDB(Base):
    __tablename__ = "companies"

    Company_ID = Column(String, primary_key=True)
    Name = Column(String, nullable=False)
    Gstin = Column(String, unique=True, nullable=False)
    Address = Column(String)
    Password = Column(String, nullable=False)
    Domain = Column(String)

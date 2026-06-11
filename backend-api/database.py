import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

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


# ---------- Create all tables ----------

Base.metadata.create_all(bind=engine)


# ---------- DB session dependency ----------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

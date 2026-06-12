from sqlalchemy import Column, String
from database import Base


class EmployeeDB(Base):
    __tablename__ = "employees"

    Employee_ID = Column(String, primary_key=True)
    Name = Column(String, nullable=False)
    Email = Column(String, unique=True, nullable=False)
    Password = Column(String, nullable=False)
    PanNumber = Column(String, unique=True, nullable=False)

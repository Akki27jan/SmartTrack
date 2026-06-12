from pydantic import BaseModel, EmailStr


class Employee(BaseModel):
    Employee_ID: str
    Name: str
    Email: EmailStr
    Password: str
    PanNumber: str


class EmployeeSignup(BaseModel):
    Name: str
    Email: EmailStr
    Password: str
    PanNumber: str


class EmployeeLogin(BaseModel):
    Email: EmailStr
    Password: str

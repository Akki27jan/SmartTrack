from pydantic import BaseModel


class EmployeeNotification(BaseModel):
    Employee_ID: str
    Type: str
    Subject: str
    Message: str


class CompanyNotification(BaseModel):
    Company_ID: str
    Type: str
    Subject: str
    Message: str

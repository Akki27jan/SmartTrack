from pydantic import BaseModel


class Company(BaseModel):
    Company_ID: str
    Name: str
    Gstin: str
    Address: str
    Password: str
    Domain: str


class CompanySignup(BaseModel):
    Name: str
    Gstin: str
    Address: str
    Password: str
    Domain: str


class CompanyLogin(BaseModel):
    Gstin: str
    Password: str

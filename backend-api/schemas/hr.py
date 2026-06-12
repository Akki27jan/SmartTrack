from pydantic import BaseModel, EmailStr


class CompanyHR(BaseModel):
    HR_ID: str
    Company_ID: str
    Name: str
    Company_Email: EmailStr
    Password: str


class HRSignup(BaseModel):
    Company_ID: str
    Name: str
    Company_Email: EmailStr
    Password: str


class HRLogin(BaseModel):
    Company_Email: EmailStr
    Password: str

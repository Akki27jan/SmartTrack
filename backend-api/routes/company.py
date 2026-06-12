from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.company import CompanyDB
from schemas.company import CompanySignup, CompanyLogin
from utils.id_generator import generate_custom_id

router = APIRouter()


@router.post("/company/signup")
def company_signup(data: CompanySignup, db: Session = Depends(get_db)):
    # Check for duplicate GSTIN
    existing = db.query(CompanyDB).filter(CompanyDB.Gstin == data.Gstin).first()
    if existing:
        raise HTTPException(status_code=400, detail="A company with this GSTIN already exists")

    custom_id = generate_custom_id(data.Name, "C", db, CompanyDB, CompanyDB.Company_ID)

    new_company = CompanyDB(
        Company_ID=custom_id,
        Name=data.Name,
        Gstin=data.Gstin,
        Address=data.Address,
        Password=data.Password,
        Domain=data.Domain
    )
    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return {"message": "Company registered successfully", "Company_ID": custom_id}


@router.post("/company/login")
def company_login(data: CompanyLogin, db: Session = Depends(get_db)):
    company = db.query(CompanyDB).filter(
        CompanyDB.Gstin == data.Gstin,
        CompanyDB.Password == data.Password
    ).first()
    if company:
        return {"message": "Company login successful", "Company_ID": company.Company_ID, "Name": company.Name}
    raise HTTPException(status_code=401, detail="Invalid GSTIN or password")

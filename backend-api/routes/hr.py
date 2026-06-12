from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.company import CompanyDB
from models.hr import CompanyHRDB
from schemas.hr import HRSignup, HRLogin
from utils.id_generator import generate_custom_id

router = APIRouter()


@router.post("/hr/signup")
def hr_signup(data: HRSignup, db: Session = Depends(get_db)):
    # Verify that the Company_ID exists
    company = db.query(CompanyDB).filter(CompanyDB.Company_ID == data.Company_ID).first()
    if not company:
        raise HTTPException(status_code=400, detail="Company Does Not Exist")

    # Check for duplicate company email
    existing = db.query(CompanyHRDB).filter(CompanyHRDB.Company_Email == data.Company_Email).first()
    if existing:
        raise HTTPException(status_code=400, detail="An HR with this company email already exists")

    custom_id = generate_custom_id(data.Name, "H", db, CompanyHRDB, CompanyHRDB.HR_ID)

    new_hr = CompanyHRDB(
        HR_ID=custom_id,
        Company_ID=data.Company_ID,
        Name=data.Name,
        Company_Email=data.Company_Email,
        Password=data.Password
    )
    db.add(new_hr)
    db.commit()
    db.refresh(new_hr)

    return {"message": "HR registered successfully", "HR_ID": custom_id}


@router.post("/hr/login")
def hr_login(data: HRLogin, db: Session = Depends(get_db)):
    hr = db.query(CompanyHRDB).filter(
        CompanyHRDB.Company_Email == data.Company_Email,
        CompanyHRDB.Password == data.Password
    ).first()
    if hr:
        return {"message": "HR login successful", "HR_ID": hr.HR_ID, "Name": hr.Name}
    raise HTTPException(status_code=401, detail="Invalid company email or password")

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.employee import EmployeeDB
from schemas.employee import EmployeeSignup, EmployeeLogin
from utils.id_generator import generate_custom_id

router = APIRouter()


@router.post("/employee/signup")
def employee_signup(data: EmployeeSignup, db: Session = Depends(get_db)):
    # Check for duplicate email
    existing_email = db.query(EmployeeDB).filter(EmployeeDB.Email == data.Email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="An employee with this email already exists")

    # Check for duplicate PAN
    existing_pan = db.query(EmployeeDB).filter(EmployeeDB.PanNumber == data.PanNumber).first()
    if existing_pan:
        raise HTTPException(status_code=400, detail="An employee with this PAN already exists")

    custom_id = generate_custom_id(data.Name, "E", db, EmployeeDB, EmployeeDB.Employee_ID)

    new_employee = EmployeeDB(
        Employee_ID=custom_id,
        Name=data.Name,
        Email=data.Email,
        Password=data.Password,
        PanNumber=data.PanNumber
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return {"message": "Employee registered successfully", "Employee_ID": custom_id}


@router.post("/employee/login")
def employee_login(data: EmployeeLogin, db: Session = Depends(get_db)):
    emp = db.query(EmployeeDB).filter(
        EmployeeDB.Email == data.Email,
        EmployeeDB.Password == data.Password
    ).first()
    if emp:
        return {"message": "Employee login successful", "Employee_ID": emp.Employee_ID, "Name": emp.Name}
    raise HTTPException(status_code=401, detail="Invalid email or password")

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.hr import CompanyHRDB
from models.employee import EmployeeDB
from models.employee_record import EmployeeRecordDB
from schemas.employee_record import EmployeeRecordCreate
from utils.id_generator import generate_record_id

router = APIRouter()


@router.post("/employee-record")
def create_employee_record(data: EmployeeRecordCreate, db: Session = Depends(get_db)):
    # Authenticate HR and get their Company_ID
    hr = db.query(CompanyHRDB).filter(CompanyHRDB.HR_ID == data.HR_ID).first()
    if not hr:
        raise HTTPException(status_code=401, detail="Invalid HR ID or HR not found")

    # Verify Employee exists
    employee = db.query(EmployeeDB).filter(EmployeeDB.Employee_ID == data.Employee_ID).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    record_id = generate_record_id(db)

    new_record = EmployeeRecordDB(
        Record_ID=record_id,
        Employee_ID=data.Employee_ID,
        Company_ID=hr.Company_ID,  # Implicitly bound to the HR's company
        Department=data.Department,
        Designation=data.Designation,
        Joining_Date=data.Joining_Date,
        Leaving_Date=data.Leaving_Date,
        Reason_of_Exit=data.Reason_of_Exit,
        Rating=data.Rating,
        Conduct_Flags=data.Conduct_Flags,
        Would_Hire=data.Would_Hire,
        Additional_Notes=data.Additional_Notes
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return {"message": "Employee record created successfully", "Record_ID": record_id}


@router.get("/employee/{employee_id}/records")
def get_employee_records(employee_id: str, db: Session = Depends(get_db)):
    records = db.query(EmployeeRecordDB).filter(EmployeeRecordDB.Employee_ID == employee_id).all()
    return records

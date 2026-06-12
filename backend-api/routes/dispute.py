from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from models.employee import EmployeeDB
from models.company import CompanyDB
from models.dispute import EmployeeDisputeDB, DisputeResponseDB, EvidenceDB
from schemas.dispute import EmployeeDispute, DisputeResponse, Evidence, ResolveDispute
from utils.id_generator import generate_dispute_id, generate_response_id, generate_evidence_id

router = APIRouter()


@router.post("/employee/dispute")
def raise_employee_dispute(data: EmployeeDispute, db: Session = Depends(get_db)):
    employee = db.query(EmployeeDB).filter(EmployeeDB.Employee_ID == data.Raised_By).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    company = db.query(CompanyDB).filter(CompanyDB.Company_ID == data.Raised_Against).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    dispute_id = generate_dispute_id(db)

    dispute = EmployeeDisputeDB(
        Dispute_ID=dispute_id,
        Raised_By=data.Raised_By,
        Raised_Against=data.Raised_Against,
        Dispute_Type=data.Dispute_Type,
        Description=data.Description,
        Status="Open"
    )

    db.add(dispute)
    db.commit()
    db.refresh(dispute)

    return {
        "message": "Dispute raised successfully",
        "Dispute_ID": dispute_id
    }


@router.get("/employee/{employee_id}/disputes")
def get_employee_disputes(employee_id: str, db: Session = Depends(get_db)):
    disputes = db.query(EmployeeDisputeDB).filter(
        EmployeeDisputeDB.Raised_By == employee_id
    ).all()

    return disputes


@router.get("/company/{company_id}/disputes")
def get_company_disputes(company_id: str, db: Session = Depends(get_db)):
    disputes = db.query(EmployeeDisputeDB).filter(
        EmployeeDisputeDB.Raised_Against == company_id
    ).all()

    return disputes


@router.post("/dispute/response")
def create_dispute_response(data: DisputeResponse, db: Session = Depends(get_db)):
    dispute = db.query(EmployeeDisputeDB).filter(
        EmployeeDisputeDB.Dispute_ID == data.Dispute_ID
    ).first()

    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found")

    response_id = generate_response_id(db)

    response = DisputeResponseDB(
        Response_ID=response_id,
        Dispute_ID=data.Dispute_ID
    )

    db.add(response)
    db.commit()
    db.refresh(response)

    return {
        "message": "Dispute response added",
        "Response_ID": response_id
    }


@router.post("/dispute/evidence")
def upload_evidence(data: Evidence, db: Session = Depends(get_db)):
    dispute = db.query(EmployeeDisputeDB).filter(
        EmployeeDisputeDB.Dispute_ID == data.Dispute_ID
    ).first()

    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found")

    evidence_id = generate_evidence_id(db)

    evidence = EvidenceDB(
        Evidence_ID=evidence_id,
        Response_ID=data.Response_ID,
        Dispute_ID=data.Dispute_ID,
        File_Url=data.File_Url,
        Uploaded_By=data.Uploaded_By
    )

    db.add(evidence)
    db.commit()
    db.refresh(evidence)

    return {
        "message": "Evidence uploaded successfully",
        "Evidence_ID": evidence_id
    }


@router.put("/dispute/{dispute_id}/resolve")
def resolve_dispute(dispute_id: str, data: ResolveDispute, db: Session = Depends(get_db)):
    dispute = db.query(EmployeeDisputeDB).filter(
        EmployeeDisputeDB.Dispute_ID == dispute_id
    ).first()

    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found")

    dispute.Status = data.Status
    dispute.Resolve_Time = datetime.utcnow()

    db.commit()
    db.refresh(dispute)

    return {
        "message": "Dispute status updated",
        "Dispute_ID": dispute.Dispute_ID,
        "Status": dispute.Status
    }

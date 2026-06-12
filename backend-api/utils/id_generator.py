from sqlalchemy.orm import Session


def generate_custom_id(name: str, type_char: str, db: Session, model_class, id_column) -> str:
    """Generate a custom ID in the format AAT000.
    AA = first 2 letters of name (uppercased)
    T  = type char (C for company, E for employee, H for HR)
    000 = incrementing number based on total existing records
    """
    prefix = name[:2].upper()
    count = db.query(model_class).count()
    number = str(count + 1).zfill(3)
    return f"{prefix}{type_char}{number}"


def generate_audit_log_id(db: Session) -> str:
    """Generate an Audit Log ID in the format AUD000."""
    from models.audit import AuditLogDB
    count = db.query(AuditLogDB).count()
    number = str(count + 1).zfill(3)
    return f"AUD{number}"


def generate_dispute_id(db: Session) -> str:
    """Generate a Dispute ID in the format DIS000."""
    from models.dispute import EmployeeDisputeDB
    count = db.query(EmployeeDisputeDB).count()
    return f"DIS{str(count + 1).zfill(3)}"


def generate_response_id(db: Session) -> str:
    """Generate a Response ID in the format RES000."""
    from models.dispute import DisputeResponseDB
    count = db.query(DisputeResponseDB).count()
    return f"RES{str(count + 1).zfill(3)}"


def generate_evidence_id(db: Session) -> str:
    """Generate an Evidence ID in the format EVD000."""
    from models.dispute import EvidenceDB
    count = db.query(EvidenceDB).count()
    return f"EVD{str(count + 1).zfill(3)}"


def generate_record_id(db: Session) -> str:
    """Generate a Record ID in the format REC000."""
    from models.employee_record import EmployeeRecordDB
    count = db.query(EmployeeRecordDB).count()
    return f"REC{str(count + 1).zfill(3)}"

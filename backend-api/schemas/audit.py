from pydantic import BaseModel


class AuditLog(BaseModel):
    HR_ID: str
    Action_Type: str
    Employee_ID: str

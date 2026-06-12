from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


class EmployeeRecordCreate(BaseModel):
    HR_ID: str
    Employee_ID: str
    Department: str
    Designation: str
    Joining_Date: datetime
    Leaving_Date: Optional[datetime] = None
    Reason_of_Exit: Optional[str] = None
    Rating: Decimal
    Conduct_Flags: Optional[str] = None
    Would_Hire: str
    Additional_Notes: Optional[str] = None

from pydantic import BaseModel


class EmployeeDispute(BaseModel):
    Raised_By: str
    Raised_Against: str
    Dispute_Type: str
    Description: str


class DisputeResponse(BaseModel):
    Dispute_ID: str


class Evidence(BaseModel):
    Response_ID: str | None = None
    Dispute_ID: str
    File_Url: str
    Uploaded_By: str


class ResolveDispute(BaseModel):
    Status: str

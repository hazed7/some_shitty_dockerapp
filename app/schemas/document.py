from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
import uuid

class DocumentSchema(BaseModel):
    document_id: Optional[uuid.UUID] = Field(None, description="Unique identifier for the document")
    person_id: uuid.UUID = Field(..., description="Unique identifier for the person")
    document_type: str
    start_date: Optional[date]
    end_date: Optional[date]

    class Config:
        from_attributes = True
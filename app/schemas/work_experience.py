from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
import uuid

class WorkExperienceSchema(BaseModel):
    experience_id: Optional[uuid.UUID] = Field(None, description="Unique identifier for the work experience")
    person_id: uuid.UUID = Field(..., description="Unique identifier for the person")
    company_name: str
    job_title: str
    start_date: Optional[date]
    end_date: Optional[date]
    rate_worked: Optional[float]

    class Config:
        from_attributes = True

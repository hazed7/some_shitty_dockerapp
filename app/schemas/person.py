from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
import uuid

class PersonSchema(BaseModel):
    person_id: Optional[uuid.UUID] = Field(None, description="Unique identifier for the person")
    full_name: str
    phone_number: str
    date_of_birth: date
    consent_to_personal_data: bool

    class Config:
        from_attributes = True
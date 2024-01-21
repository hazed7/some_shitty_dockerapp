from pydantic import BaseModel, Field
from typing import Optional
import uuid

class AddressSchema(BaseModel):
    address_id: Optional[uuid.UUID] = Field(None, description="Unique identifier for the address")
    person_id: uuid.UUID
    address: str

    class Config:
        from_attributes = True

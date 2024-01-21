from pydantic import BaseModel, Field
from typing import Optional
import uuid

class RelativeSchema(BaseModel):
    relative_id: Optional[uuid.UUID] = Field(None, description="Unique identifier for the relative")
    person_id: uuid.UUID
    relative_name: str
    relation_type: str

    class Config:
        from_attributes = True

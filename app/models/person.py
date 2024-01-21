from sqlalchemy import Column, String, Date, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base

class Person(Base):
    __tablename__ = 'persons'

    person_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    full_name = Column(String, nullable=False)
    phone_number = Column(String, unique=True)
    date_of_birth = Column(Date)
    consent_to_personal_data = Column(Boolean, nullable=False, default=False)

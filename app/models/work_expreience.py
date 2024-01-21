from sqlalchemy import Column, ForeignKey, String, Date, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base
from sqlalchemy.sql import text
import uuid

class WorkExperience(Base):
    __tablename__ = 'work_experience'

    experience_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    person_id = Column(UUID(as_uuid=True), ForeignKey('persons.person_id'), nullable=False)
    company_name = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    rate_worked = Column(DECIMAL(10, 2))

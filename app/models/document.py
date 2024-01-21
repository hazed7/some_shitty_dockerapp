from sqlalchemy import Column, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base
import uuid

class Document(Base):
    __tablename__ = 'documents'

    document_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    person_id = Column(UUID(as_uuid=True), ForeignKey('persons.person_id'), nullable=False)
    document_type = Column(String, nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
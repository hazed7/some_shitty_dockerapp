from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base
from sqlalchemy.sql import text
import uuid

class Relative(Base):
    __tablename__ = 'relatives'

    relative_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    person_id = Column(UUID(as_uuid=True), ForeignKey('persons.person_id'), nullable=False)
    relative_name = Column(String, nullable=False)
    relation_type = Column(String, nullable=False)

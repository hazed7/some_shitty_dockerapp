from sqlalchemy import Column, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base
import uuid

class Address(Base):
    __tablename__ = 'addresses'

    address_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    person_id = Column(UUID(as_uuid=True), ForeignKey('persons.person_id'), nullable=False)
    address = Column(Text, nullable=False)

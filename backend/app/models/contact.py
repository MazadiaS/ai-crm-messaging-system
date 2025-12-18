from datetime import datetime, date
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Date, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import enum

from app.config.database import Base


class ContactSegment(str, enum.Enum):
    """Contact segment categories"""
    VIP = "VIP"
    REGULAR = "regular"
    NEW_CLIENT = "new_client"
    PARTNER = "partner"


class Language(str, enum.Enum):
    """Supported languages"""
    RU = "ru"
    EN = "en"
    UZ = "uz"


class Contact(Base):
    """Contact model for CRM"""

    __tablename__ = "contacts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, nullable=True)
    segment = Column(Enum(ContactSegment), default=ContactSegment.REGULAR, nullable=False, index=True)
    birthday = Column(Date, nullable=True, index=True)
    company = Column(String, nullable=True)
    position = Column(String, nullable=True)
    language = Column(Enum(Language), default=Language.RU, nullable=False)
    tags = Column(JSONB, default=list, nullable=True)
    custom_fields = Column(JSONB, default=dict, nullable=True)
    last_interaction_date = Column(DateTime, nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    creator = relationship("User", foreign_keys=[created_by])

    def __repr__(self):
        return f"<Contact {self.name} ({self.email})>"

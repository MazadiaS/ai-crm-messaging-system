from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Text, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.config.database import Base
from app.models.message import OccasionType
from app.models.contact import ContactSegment, Language


class Template(Base):
    """Template model for pre-written message templates"""

    __tablename__ = "templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    name = Column(String, nullable=False)
    occasion_type = Column(Enum(OccasionType), nullable=False, index=True)
    segment = Column(Enum(ContactSegment), nullable=True, index=True)
    content = Column(Text, nullable=False)
    language = Column(Enum(Language), default=Language.RU, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    usage_count = Column(Integer, default=0, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    creator = relationship("User", foreign_keys=[created_by])

    def __repr__(self):
        return f"<Template {self.name} - {self.occasion_type}>"

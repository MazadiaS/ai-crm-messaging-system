from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import enum

from app.config.database import Base


class OccasionType(str, enum.Enum):
    """Message occasion types"""
    BIRTHDAY = "birthday"
    NEW_YEAR = "new_year"
    HOLIDAY = "holiday"
    PROMOTION = "promotion"
    CUSTOM = "custom"


class MessageStatus(str, enum.Enum):
    """Message status workflow"""
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    SENT = "sent"
    FAILED = "failed"
    REJECTED = "rejected"


class GeneratedBy(str, enum.Enum):
    """Message generation source"""
    AI = "AI"
    MANUAL = "manual"


class Message(Base):
    """Message model for CRM communications"""

    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    contact_id = Column(UUID(as_uuid=True), ForeignKey("contacts.id"), nullable=False, index=True)
    occasion_type = Column(Enum(OccasionType), nullable=False, index=True)
    content = Column(Text, nullable=False)
    status = Column(Enum(MessageStatus), default=MessageStatus.DRAFT, nullable=False, index=True)
    generated_by = Column(Enum(GeneratedBy), default=GeneratedBy.MANUAL, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    sent_at = Column(DateTime, nullable=True)
    approved_at = Column(DateTime, nullable=True)
    scheduled_for = Column(DateTime, nullable=True, index=True)
    message_metadata = Column(JSONB, default=dict, nullable=True)  # AI model version, tokens, etc.
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    contact = relationship("Contact", foreign_keys=[contact_id])
    creator = relationship("User", foreign_keys=[created_by])
    approver = relationship("User", foreign_keys=[approved_by])

    def __repr__(self):
        return f"<Message {self.id} - {self.status}>"


class MessageHistory(Base):
    """Message audit trail"""

    __tablename__ = "message_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    message_id = Column(UUID(as_uuid=True), ForeignKey("messages.id"), nullable=False, index=True)
    action = Column(String, nullable=False)  # created, edited, approved, rejected, sent
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    old_content = Column(Text, nullable=True)
    new_content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    message = relationship("Message", foreign_keys=[message_id])
    user = relationship("User", foreign_keys=[user_id])

    def __repr__(self):
        return f"<MessageHistory {self.action} - {self.created_at}>"

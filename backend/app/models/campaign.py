from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import enum

from app.config.database import Base
from app.models.message import OccasionType


class ScheduleType(str, enum.Enum):
    """Campaign schedule types"""
    IMMEDIATE = "immediate"
    SCHEDULED = "scheduled"
    RECURRING = "recurring"


class CampaignStatus(str, enum.Enum):
    """Campaign status"""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"


class Campaign(Base):
    """Campaign model for bulk message operations"""

    __tablename__ = "campaigns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    occasion_type = Column(Enum(OccasionType), nullable=False)
    segment_filter = Column(JSONB, default=dict, nullable=True)  # Which segments to target
    schedule_type = Column(Enum(ScheduleType), default=ScheduleType.IMMEDIATE, nullable=False)
    scheduled_at = Column(DateTime, nullable=True)
    recurrence_rule = Column(String, nullable=True)  # Cron expression
    status = Column(Enum(CampaignStatus), default=CampaignStatus.DRAFT, nullable=False, index=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    stats = Column(JSONB, default=dict, nullable=True)  # generated_count, sent_count, etc.
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    creator = relationship("User", foreign_keys=[created_by])

    def __repr__(self):
        return f"<Campaign {self.name} - {self.status}>"

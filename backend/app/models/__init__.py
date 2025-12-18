"""Database models"""

from app.config.database import Base
from app.models.user import User, UserRole
from app.models.contact import Contact, ContactSegment, Language
from app.models.message import Message, MessageHistory, MessageStatus, OccasionType, GeneratedBy
from app.models.campaign import Campaign, CampaignStatus, ScheduleType
from app.models.template import Template

__all__ = [
    "Base",
    "User",
    "UserRole",
    "Contact",
    "ContactSegment",
    "Language",
    "Message",
    "MessageHistory",
    "MessageStatus",
    "OccasionType",
    "GeneratedBy",
    "Campaign",
    "CampaignStatus",
    "ScheduleType",
    "Template",
]

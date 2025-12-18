from datetime import datetime
from uuid import UUID
from typing import Dict, List, Any
from pydantic import BaseModel, Field

from app.models.message import OccasionType, MessageStatus, GeneratedBy


# Request schemas
class MessageGenerate(BaseModel):
    """Schema for generating a new message with AI"""
    contact_id: UUID
    occasion_type: OccasionType
    custom_context: str | None = Field(None, max_length=500)
    tone: str = Field("professional_friendly", max_length=50)


class MessageCreate(BaseModel):
    """Schema for manually creating a message"""
    contact_id: UUID
    occasion_type: OccasionType
    content: str = Field(..., min_length=10, max_length=2000)


class MessageUpdate(BaseModel):
    """Schema for updating a message"""
    content: str | None = Field(None, min_length=10, max_length=2000)
    scheduled_for: datetime | None = None


class MessageFilter(BaseModel):
    """Schema for filtering messages"""
    status: MessageStatus | None = None
    occasion_type: OccasionType | None = None
    contact_id: UUID | None = None
    generated_by: GeneratedBy | None = None
    search: str | None = None
    skip: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)


# Response schemas
class MessageResponse(BaseModel):
    """Schema for message response"""
    id: UUID
    contact_id: UUID
    occasion_type: OccasionType
    content: str
    status: MessageStatus
    generated_by: GeneratedBy
    created_by: UUID
    approved_by: UUID | None
    sent_at: datetime | None
    approved_at: datetime | None
    scheduled_for: datetime | None
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class MessageWithContact(MessageResponse):
    """Schema for message with contact details"""
    contact_name: str
    contact_email: str


class MessageListResponse(BaseModel):
    """Schema for paginated message list"""
    items: List[MessageResponse]
    total: int
    skip: int
    limit: int


class MessageHistoryResponse(BaseModel):
    """Schema for message history entry"""
    id: UUID
    message_id: UUID
    action: str
    user_id: UUID
    old_content: str | None
    new_content: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class MessageApprove(BaseModel):
    """Schema for approving a message"""
    pass  # No additional fields needed


class MessageReject(BaseModel):
    """Schema for rejecting a message"""
    reason: str | None = Field(None, max_length=500)

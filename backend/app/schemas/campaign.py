from datetime import datetime
from uuid import UUID
from typing import Dict, List, Any
from pydantic import BaseModel, Field

from app.models.campaign import ScheduleType, CampaignStatus
from app.models.message import OccasionType


# Request schemas
class CampaignCreate(BaseModel):
    """Schema for creating a new campaign"""
    name: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
    occasion_type: OccasionType
    segment_filter: Dict[str, Any] = Field(default_factory=dict)
    schedule_type: ScheduleType = ScheduleType.IMMEDIATE
    scheduled_at: datetime | None = None
    recurrence_rule: str | None = Field(None, max_length=100)


class CampaignUpdate(BaseModel):
    """Schema for updating a campaign"""
    name: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
    occasion_type: OccasionType | None = None
    segment_filter: Dict[str, Any] | None = None
    schedule_type: ScheduleType | None = None
    scheduled_at: datetime | None = None
    recurrence_rule: str | None = Field(None, max_length=100)
    status: CampaignStatus | None = None


class CampaignFilter(BaseModel):
    """Schema for filtering campaigns"""
    status: CampaignStatus | None = None
    occasion_type: OccasionType | None = None
    skip: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)


# Response schemas
class CampaignResponse(BaseModel):
    """Schema for campaign response"""
    id: UUID
    name: str
    description: str | None
    occasion_type: OccasionType
    segment_filter: Dict[str, Any]
    schedule_type: ScheduleType
    scheduled_at: datetime | None
    recurrence_rule: str | None
    status: CampaignStatus
    created_by: UUID
    stats: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CampaignListResponse(BaseModel):
    """Schema for paginated campaign list"""
    items: List[CampaignResponse]
    total: int
    skip: int
    limit: int


class CampaignExecute(BaseModel):
    """Schema for executing a campaign"""
    test_mode: bool = False  # If True, only generate but don't send

from datetime import datetime
from uuid import UUID
from typing import List
from pydantic import BaseModel, Field

from app.models.message import OccasionType
from app.models.contact import ContactSegment, Language


# Request schemas
class TemplateCreate(BaseModel):
    """Schema for creating a new template"""
    name: str = Field(..., min_length=1, max_length=200)
    occasion_type: OccasionType
    segment: ContactSegment | None = None
    content: str = Field(..., min_length=10, max_length=2000)
    language: Language = Language.RU
    is_active: bool = True


class TemplateUpdate(BaseModel):
    """Schema for updating a template"""
    name: str | None = Field(None, min_length=1, max_length=200)
    occasion_type: OccasionType | None = None
    segment: ContactSegment | None = None
    content: str | None = Field(None, min_length=10, max_length=2000)
    language: Language | None = None
    is_active: bool | None = None


class TemplateFilter(BaseModel):
    """Schema for filtering templates"""
    occasion_type: OccasionType | None = None
    segment: ContactSegment | None = None
    language: Language | None = None
    is_active: bool | None = None
    skip: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)


# Response schemas
class TemplateResponse(BaseModel):
    """Schema for template response"""
    id: UUID
    name: str
    occasion_type: OccasionType
    segment: ContactSegment | None
    content: str
    language: Language
    is_active: bool
    usage_count: int
    created_by: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TemplateListResponse(BaseModel):
    """Schema for paginated template list"""
    items: List[TemplateResponse]
    total: int
    skip: int
    limit: int

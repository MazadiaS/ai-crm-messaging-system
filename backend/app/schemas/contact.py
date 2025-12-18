from datetime import datetime, date
from uuid import UUID
from typing import Dict, List, Any
from pydantic import BaseModel, EmailStr, Field

from app.models.contact import ContactSegment, Language


# Request schemas
class ContactCreate(BaseModel):
    """Schema for creating a new contact"""
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    phone: str | None = Field(None, max_length=50)
    segment: ContactSegment = ContactSegment.REGULAR
    birthday: date | None = None
    company: str | None = Field(None, max_length=200)
    position: str | None = Field(None, max_length=200)
    language: Language = Language.RU
    tags: List[str] = Field(default_factory=list)
    custom_fields: Dict[str, Any] = Field(default_factory=dict)


class ContactUpdate(BaseModel):
    """Schema for updating a contact"""
    name: str | None = Field(None, min_length=1, max_length=200)
    email: EmailStr | None = None
    phone: str | None = Field(None, max_length=50)
    segment: ContactSegment | None = None
    birthday: date | None = None
    company: str | None = Field(None, max_length=200)
    position: str | None = Field(None, max_length=200)
    language: Language | None = None
    tags: List[str] | None = None
    custom_fields: Dict[str, Any] | None = None


class ContactFilter(BaseModel):
    """Schema for filtering contacts"""
    segment: ContactSegment | None = None
    language: Language | None = None
    search: str | None = None  # Search in name, email, company
    has_birthday_this_month: bool | None = None
    skip: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)


# Response schemas
class ContactResponse(BaseModel):
    """Schema for contact response"""
    id: UUID
    name: str
    email: str
    phone: str | None
    segment: ContactSegment
    birthday: date | None
    company: str | None
    position: str | None
    language: Language
    tags: List[str]
    custom_fields: Dict[str, Any]
    last_interaction_date: datetime | None
    created_by: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ContactListResponse(BaseModel):
    """Schema for paginated contact list"""
    items: List[ContactResponse]
    total: int
    skip: int
    limit: int

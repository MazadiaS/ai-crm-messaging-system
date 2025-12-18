from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

from app.models.user import UserRole


# Request schemas
class UserCreate(BaseModel):
    """Schema for creating a new user"""
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)
    role: UserRole = UserRole.VIEWER


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Schema for updating user"""
    full_name: str | None = Field(None, min_length=1, max_length=100)
    role: UserRole | None = None


# Response schemas
class UserResponse(BaseModel):
    """Schema for user response"""
    id: UUID
    email: str
    full_name: str
    role: UserRole
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    """Schema for authentication token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse

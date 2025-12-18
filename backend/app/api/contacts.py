"""Contacts API endpoints"""

from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, extract
from datetime import datetime

from app.config.database import get_db
from app.models.contact import Contact
from app.schemas.contact import (
    ContactCreate,
    ContactUpdate,
    ContactResponse,
    ContactListResponse,
    ContactFilter
)
from app.api.deps import CurrentUser

router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.get("", response_model=ContactListResponse)
async def list_contacts(
    segment: str | None = None,
    language: str | None = None,
    search: str | None = None,
    has_birthday_this_month: bool | None = None,
    skip: int = 0,
    limit: int = 20,
    db: Annotated[AsyncSession, Depends(get_db)] = Depends(),
    current_user: CurrentUser = Depends(),
):
    """List contacts with filtering and pagination"""

    # Build query
    query = select(Contact)

    # Apply filters
    if segment:
        query = query.where(Contact.segment == segment)

    if language:
        query = query.where(Contact.language == language)

    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            or_(
                Contact.name.ilike(search_pattern),
                Contact.email.ilike(search_pattern),
                Contact.company.ilike(search_pattern)
            )
        )

    if has_birthday_this_month:
        current_month = datetime.utcnow().month
        query = query.where(extract('month', Contact.birthday) == current_month)

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Apply pagination
    query = query.offset(skip).limit(limit).order_by(Contact.created_at.desc())

    # Execute query
    result = await db.execute(query)
    contacts = result.scalars().all()

    return ContactListResponse(
        items=[ContactResponse.model_validate(contact) for contact in contacts],
        total=total,
        skip=skip,
        limit=limit
    )


@router.post("", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
    contact_data: ContactCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser
):
    """Create a new contact"""

    # Check if email already exists
    result = await db.execute(select(Contact).where(Contact.email == contact_data.email))
    existing_contact = result.scalar_one_or_none()

    if existing_contact:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contact with this email already exists"
        )

    # Create contact
    contact = Contact(
        **contact_data.model_dump(),
        created_by=current_user.id
    )

    db.add(contact)
    await db.commit()
    await db.refresh(contact)

    return ContactResponse.model_validate(contact)


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser
):
    """Get a specific contact by ID"""

    result = await db.execute(select(Contact).where(Contact.id == contact_id))
    contact = result.scalar_one_or_none()

    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )

    return ContactResponse.model_validate(contact)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: UUID,
    contact_data: ContactUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser
):
    """Update a contact"""

    # Get contact
    result = await db.execute(select(Contact).where(Contact.id == contact_id))
    contact = result.scalar_one_or_none()

    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )

    # Check email uniqueness if email is being updated
    if contact_data.email and contact_data.email != contact.email:
        email_result = await db.execute(
            select(Contact).where(Contact.email == contact_data.email)
        )
        if email_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contact with this email already exists"
            )

    # Update contact
    update_data = contact_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(contact, key, value)

    await db.commit()
    await db.refresh(contact)

    return ContactResponse.model_validate(contact)


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
    contact_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser
):
    """Delete a contact"""

    result = await db.execute(select(Contact).where(Contact.id == contact_id))
    contact = result.scalar_one_or_none()

    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )

    await db.delete(contact)
    await db.commit()

    return None


@router.post("/import")
async def import_contacts(
    file: UploadFile = File(...),
    db: Annotated[AsyncSession, Depends(get_db)] = Depends(),
    current_user: CurrentUser = Depends(),
):
    """Import contacts from CSV file (placeholder for Celery task)"""

    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV files are supported"
        )

    # TODO: Implement Celery task for bulk import
    # For now, return a placeholder response

    return {
        "message": "Import queued",
        "filename": file.filename,
        "status": "processing"
    }


@router.get("/export/csv")
async def export_contacts(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser
):
    """Export contacts to CSV (placeholder)"""

    # TODO: Implement CSV export
    return {"message": "Export feature coming soon"}

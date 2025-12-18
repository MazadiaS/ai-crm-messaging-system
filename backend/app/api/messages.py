"""Messages API endpoints"""

from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from datetime import datetime

from app.config.database import get_db
from app.models.contact import Contact
from app.models.message import Message, MessageHistory, MessageStatus, GeneratedBy
from app.schemas.message import (
    MessageGenerate,
    MessageCreate,
    MessageUpdate,
    MessageResponse,
    MessageListResponse,
    MessageHistoryResponse,
    MessageApprove,
    MessageReject
)
from app.services.ai_generator import ai_generator
from app.api.deps import CurrentUser

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post("/generate", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def generate_message(
    message_data: MessageGenerate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser
):
    """Generate a personalized message using AI"""

    # Get contact
    contact_result = await db.execute(
        select(Contact).where(Contact.id == message_data.contact_id)
    )
    contact = contact_result.scalar_one_or_none()

    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )

    # Generate message with AI
    generation_result = ai_generator.generate_personalized_message(
        contact=contact,
        occasion_type=message_data.occasion_type,
        custom_context=message_data.custom_context,
        tone=message_data.tone
    )

    if not generation_result["success"]:
        # Use fallback message
        content = ai_generator.get_fallback_message(
            contact_name=contact.name,
            occasion_type=message_data.occasion_type,
            language=contact.language.value
        )
        metadata = generation_result["metadata"]
        metadata["fallback_used"] = True
        metadata["error"] = generation_result["error"]
    else:
        content = generation_result["content"]
        metadata = generation_result["metadata"]

    # Create message
    message = Message(
        contact_id=contact.id,
        occasion_type=message_data.occasion_type,
        content=content,
        status=MessageStatus.PENDING_APPROVAL,
        generated_by=GeneratedBy.AI,
        created_by=current_user.id,
        metadata=metadata
    )

    db.add(message)

    # Create history entry
    history = MessageHistory(
        message_id=message.id,
        action="created",
        user_id=current_user.id,
        new_content=content
    )
    db.add(history)

    await db.commit()
    await db.refresh(message)

    return MessageResponse.model_validate(message)


@router.post("", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message_manually(
    message_data: MessageCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser
):
    """Create a message manually (without AI)"""

    # Verify contact exists
    contact_result = await db.execute(
        select(Contact).where(Contact.id == message_data.contact_id)
    )
    contact = contact_result.scalar_one_or_none()

    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )

    # Create message
    message = Message(
        **message_data.model_dump(),
        status=MessageStatus.DRAFT,
        generated_by=GeneratedBy.MANUAL,
        created_by=current_user.id,
        metadata={"created_manually": True}
    )

    db.add(message)

    # Create history
    history = MessageHistory(
        message_id=message.id,
        action="created",
        user_id=current_user.id,
        new_content=message.content
    )
    db.add(history)

    await db.commit()
    await db.refresh(message)

    return MessageResponse.model_validate(message)


@router.get("", response_model=MessageListResponse)
async def list_messages(
    status: str | None = None,
    occasion_type: str | None = None,
    contact_id: UUID | None = None,
    generated_by: str | None = None,
    skip: int = 0,
    limit: int = 20,
    db: Annotated[AsyncSession, Depends(get_db)] = Depends(),
    current_user: CurrentUser = Depends()
):
    """List messages with filtering and pagination"""

    # Build query
    query = select(Message)

    # Apply filters
    if status:
        query = query.where(Message.status == status)

    if occasion_type:
        query = query.where(Message.occasion_type == occasion_type)

    if contact_id:
        query = query.where(Message.contact_id == contact_id)

    if generated_by:
        query = query.where(Message.generated_by == generated_by)

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Apply pagination
    query = query.offset(skip).limit(limit).order_by(Message.created_at.desc())

    # Execute query
    result = await db.execute(query)
    messages = result.scalars().all()

    return MessageListResponse(
        items=[MessageResponse.model_validate(msg) for msg in messages],
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{message_id}", response_model=MessageResponse)
async def get_message(
    message_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser
):
    """Get a specific message by ID"""

    result = await db.execute(select(Message).where(Message.id == message_id))
    message = result.scalar_one_or_none()

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )

    return MessageResponse.model_validate(message)


@router.patch("/{message_id}", response_model=MessageResponse)
async def update_message(
    message_id: UUID,
    message_data: MessageUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser
):
    """Update a message (content or schedule)"""

    # Get message
    result = await db.execute(select(Message).where(Message.id == message_id))
    message = result.scalar_one_or_none()

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )

    # Check if message can be edited
    if message.status in [MessageStatus.SENT, MessageStatus.FAILED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot edit sent or failed messages"
        )

    # Store old content for history
    old_content = message.content

    # Update message
    update_data = message_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(message, key, value)

    # Create history if content changed
    if message_data.content and message_data.content != old_content:
        history = MessageHistory(
            message_id=message.id,
            action="edited",
            user_id=current_user.id,
            old_content=old_content,
            new_content=message.content
        )
        db.add(history)

    await db.commit()
    await db.refresh(message)

    return MessageResponse.model_validate(message)


@router.post("/{message_id}/approve", response_model=MessageResponse)
async def approve_message(
    message_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser
):
    """Approve a message for sending"""

    # Get message
    result = await db.execute(select(Message).where(Message.id == message_id))
    message = result.scalar_one_or_none()

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )

    # Check current status
    if message.status not in [MessageStatus.DRAFT, MessageStatus.PENDING_APPROVAL]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only draft or pending messages can be approved"
        )

    # Update message
    message.status = MessageStatus.APPROVED
    message.approved_by = current_user.id
    message.approved_at = datetime.utcnow()

    # Create history
    history = MessageHistory(
        message_id=message.id,
        action="approved",
        user_id=current_user.id
    )
    db.add(history)

    await db.commit()
    await db.refresh(message)

    return MessageResponse.model_validate(message)


@router.post("/{message_id}/reject", response_model=MessageResponse)
async def reject_message(
    message_id: UUID,
    reject_data: MessageReject,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser
):
    """Reject a message"""

    # Get message
    result = await db.execute(select(Message).where(Message.id == message_id))
    message = result.scalar_one_or_none()

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )

    # Update message
    message.status = MessageStatus.REJECTED
    if reject_data.reason:
        message.metadata["rejection_reason"] = reject_data.reason

    # Create history
    history = MessageHistory(
        message_id=message.id,
        action="rejected",
        user_id=current_user.id
    )
    db.add(history)

    await db.commit()
    await db.refresh(message)

    return MessageResponse.model_validate(message)


@router.post("/{message_id}/send", response_model=MessageResponse)
async def send_message(
    message_id: UUID,
    background_tasks: BackgroundTasks,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser
):
    """Send a message (mock implementation for demo)"""

    # Get message
    result = await db.execute(select(Message).where(Message.id == message_id))
    message = result.scalar_one_or_none()

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )

    # Check if approved
    if message.status != MessageStatus.APPROVED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only approved messages can be sent"
        )

    # Mock sending - in production, this would be a Celery task
    message.status = MessageStatus.SENT
    message.sent_at = datetime.utcnow()

    # Create history
    history = MessageHistory(
        message_id=message.id,
        action="sent",
        user_id=current_user.id
    )
    db.add(history)

    await db.commit()
    await db.refresh(message)

    return MessageResponse.model_validate(message)


@router.get("/{message_id}/history", response_model=list[MessageHistoryResponse])
async def get_message_history(
    message_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser
):
    """Get audit trail for a message"""

    # Verify message exists
    message_result = await db.execute(select(Message).where(Message.id == message_id))
    message = message_result.scalar_one_or_none()

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )

    # Get history
    history_result = await db.execute(
        select(MessageHistory)
        .where(MessageHistory.message_id == message_id)
        .order_by(MessageHistory.created_at.desc())
    )
    history_entries = history_result.scalars().all()

    return [MessageHistoryResponse.model_validate(entry) for entry in history_entries]


@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    message_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser
):
    """Delete a message"""

    result = await db.execute(select(Message).where(Message.id == message_id))
    message = result.scalar_one_or_none()

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )

    # Don't allow deletion of sent messages
    if message.status == MessageStatus.SENT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete sent messages"
        )

    await db.delete(message)
    await db.commit()

    return None

"""Analytics API endpoints"""

from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta

from app.config.database import get_db
from app.models.message import Message, MessageStatus, OccasionType, GeneratedBy
from app.models.contact import Contact, ContactSegment
from app.models.campaign import Campaign, CampaignStatus
from app.api.deps import CurrentUser

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/dashboard")
async def get_dashboard_stats(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser
):
    """Get dashboard statistics"""

    # Total contacts
    total_contacts_result = await db.execute(select(func.count(Contact.id)))
    total_contacts = total_contacts_result.scalar()

    # Total messages
    total_messages_result = await db.execute(select(func.count(Message.id)))
    total_messages = total_messages_result.scalar()

    # Messages by status
    pending_approval_result = await db.execute(
        select(func.count(Message.id)).where(Message.status == MessageStatus.PENDING_APPROVAL)
    )
    pending_approval = pending_approval_result.scalar()

    approved_result = await db.execute(
        select(func.count(Message.id)).where(Message.status == MessageStatus.APPROVED)
    )
    approved = approved_result.scalar()

    sent_result = await db.execute(
        select(func.count(Message.id)).where(Message.status == MessageStatus.SENT)
    )
    sent = sent_result.scalar()

    # Active campaigns
    active_campaigns_result = await db.execute(
        select(func.count(Campaign.id)).where(Campaign.status == CampaignStatus.ACTIVE)
    )
    active_campaigns = active_campaigns_result.scalar()

    # Messages this month
    start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    messages_this_month_result = await db.execute(
        select(func.count(Message.id)).where(Message.created_at >= start_of_month)
    )
    messages_this_month = messages_this_month_result.scalar()

    return {
        "total_contacts": total_contacts,
        "total_messages": total_messages,
        "pending_approval": pending_approval,
        "approved": approved,
        "sent": sent,
        "active_campaigns": active_campaigns,
        "messages_this_month": messages_this_month,
        "generated_at": datetime.utcnow().isoformat()
    }


@router.get("/messages-by-status")
async def get_messages_by_status(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser
):
    """Get message counts grouped by status"""

    result = await db.execute(
        select(Message.status, func.count(Message.id))
        .group_by(Message.status)
    )

    data = [{"status": status.value, "count": count} for status, count in result.all()]

    return {"data": data}


@router.get("/messages-by-occasion")
async def get_messages_by_occasion(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser
):
    """Get message counts grouped by occasion type"""

    result = await db.execute(
        select(Message.occasion_type, func.count(Message.id))
        .group_by(Message.occasion_type)
    )

    data = [{"occasion_type": occasion.value, "count": count} for occasion, count in result.all()]

    return {"data": data}


@router.get("/ai-usage-stats")
async def get_ai_usage_stats(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser
):
    """Get AI usage statistics"""

    # Total AI-generated messages
    ai_messages_result = await db.execute(
        select(func.count(Message.id)).where(Message.generated_by == GeneratedBy.AI)
    )
    ai_messages = ai_messages_result.scalar()

    # Manual messages
    manual_messages_result = await db.execute(
        select(func.count(Message.id)).where(Message.generated_by == GeneratedBy.MANUAL)
    )
    manual_messages = manual_messages_result.scalar()

    # Get recent AI messages with metadata for token stats
    recent_ai_messages_result = await db.execute(
        select(Message.metadata)
        .where(Message.generated_by == GeneratedBy.AI)
        .where(Message.metadata.isnot(None))
        .limit(100)
    )

    total_tokens = 0
    total_cost = 0.0
    message_count = 0

    for (metadata,) in recent_ai_messages_result.all():
        if metadata:
            total_tokens += metadata.get("total_tokens", 0)
            total_cost += metadata.get("cost_usd", 0.0)
            message_count += 1

    avg_tokens = total_tokens / message_count if message_count > 0 else 0
    avg_cost = total_cost / message_count if message_count > 0 else 0

    return {
        "ai_generated": ai_messages,
        "manual": manual_messages,
        "total_tokens_used": total_tokens,
        "total_cost_usd": round(total_cost, 4),
        "avg_tokens_per_message": round(avg_tokens, 2),
        "avg_cost_per_message": round(avg_cost, 6)
    }


@router.get("/campaign-performance")
async def get_campaign_performance(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser
):
    """Get campaign performance metrics"""

    # Get all campaigns with their stats
    result = await db.execute(
        select(Campaign).order_by(Campaign.created_at.desc()).limit(10)
    )
    campaigns = result.scalars().all()

    data = []
    for campaign in campaigns:
        stats = campaign.stats or {}
        data.append({
            "id": str(campaign.id),
            "name": campaign.name,
            "status": campaign.status.value,
            "occasion_type": campaign.occasion_type.value,
            "generated_count": stats.get("generated_count", 0),
            "sent_count": stats.get("sent_count", 0),
            "failed_count": stats.get("failed_count", 0),
            "created_at": campaign.created_at.isoformat()
        })

    return {"data": data}


@router.get("/contacts-by-segment")
async def get_contacts_by_segment(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser
):
    """Get contact counts grouped by segment"""

    result = await db.execute(
        select(Contact.segment, func.count(Contact.id))
        .group_by(Contact.segment)
    )

    data = [{"segment": segment.value, "count": count} for segment, count in result.all()]

    return {"data": data}


@router.get("/messages-timeline")
async def get_messages_timeline(
    days: int = 30,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser
):
    """Get message creation timeline for the last N days"""

    # Calculate start date
    start_date = datetime.utcnow() - timedelta(days=days)

    # Get messages grouped by date
    result = await db.execute(
        select(
            func.date(Message.created_at).label('date'),
            func.count(Message.id).label('count')
        )
        .where(Message.created_at >= start_date)
        .group_by(func.date(Message.created_at))
        .order_by(func.date(Message.created_at))
    )

    data = [{"date": str(date), "count": count} for date, count in result.all()]

    return {"data": data, "days": days}

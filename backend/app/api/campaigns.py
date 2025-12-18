"""Campaigns API endpoints"""

from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.config.database import get_db
from app.models.campaign import Campaign
from app.schemas.campaign import (
    CampaignCreate,
    CampaignUpdate,
    CampaignResponse,
    CampaignListResponse,
    CampaignExecute
)
from app.api.deps import CurrentUser, ManagerUser

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])


@router.get("", response_model=CampaignListResponse)
async def list_campaigns(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser,
    status: str | None = None,
    occasion_type: str | None = None,
    skip: int = 0,
    limit: int = 20,
):
    """List campaigns with filtering and pagination"""

    query = select(Campaign)

    if status:
        query = query.where(Campaign.status == status)

    if occasion_type:
        query = query.where(Campaign.occasion_type == occasion_type)

    # Get total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Apply pagination
    query = query.offset(skip).limit(limit).order_by(Campaign.created_at.desc())

    result = await db.execute(query)
    campaigns = result.scalars().all()

    return CampaignListResponse(
        items=[CampaignResponse.model_validate(c) for c in campaigns],
        total=total,
        skip=skip,
        limit=limit
    )


@router.post("", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
async def create_campaign(
    campaign_data: CampaignCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: ManagerUser
):
    """Create a new campaign"""

    campaign = Campaign(
        **campaign_data.model_dump(),
        created_by=current_user.id,
        stats={"generated_count": 0, "sent_count": 0, "failed_count": 0}
    )

    db.add(campaign)
    await db.commit()
    await db.refresh(campaign)

    return CampaignResponse.model_validate(campaign)


@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(
    campaign_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser
):
    """Get a specific campaign"""

    result = await db.execute(select(Campaign).where(Campaign.id == campaign_id))
    campaign = result.scalar_one_or_none()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )

    return CampaignResponse.model_validate(campaign)


@router.put("/{campaign_id}", response_model=CampaignResponse)
async def update_campaign(
    campaign_id: UUID,
    campaign_data: CampaignUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: ManagerUser
):
    """Update a campaign"""

    result = await db.execute(select(Campaign).where(Campaign.id == campaign_id))
    campaign = result.scalar_one_or_none()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )

    update_data = campaign_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(campaign, key, value)

    await db.commit()
    await db.refresh(campaign)

    return CampaignResponse.model_validate(campaign)


@router.delete("/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_campaign(
    campaign_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: ManagerUser
):
    """Delete a campaign"""

    result = await db.execute(select(Campaign).where(Campaign.id == campaign_id))
    campaign = result.scalar_one_or_none()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )

    await db.delete(campaign)
    await db.commit()

    return None


@router.post("/{campaign_id}/execute")
async def execute_campaign(
    campaign_id: UUID,
    execute_data: CampaignExecute,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: ManagerUser
):
    """Execute a campaign (queue for processing)"""

    result = await db.execute(select(Campaign).where(Campaign.id == campaign_id))
    campaign = result.scalar_one_or_none()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )

    # TODO: Queue campaign execution with Celery
    # For now, return placeholder response

    return {
        "message": "Campaign execution queued",
        "campaign_id": str(campaign_id),
        "test_mode": execute_data.test_mode
    }


@router.post("/{campaign_id}/pause")
async def pause_campaign(
    campaign_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: ManagerUser
):
    """Pause an active campaign"""

    result = await db.execute(select(Campaign).where(Campaign.id == campaign_id))
    campaign = result.scalar_one_or_none()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )

    from app.models.campaign import CampaignStatus
    campaign.status = CampaignStatus.PAUSED

    await db.commit()
    await db.refresh(campaign)

    return CampaignResponse.model_validate(campaign)


@router.post("/{campaign_id}/resume")
async def resume_campaign(
    campaign_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: ManagerUser
):
    """Resume a paused campaign"""

    result = await db.execute(select(Campaign).where(Campaign.id == campaign_id))
    campaign = result.scalar_one_or_none()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )

    from app.models.campaign import CampaignStatus
    campaign.status = CampaignStatus.ACTIVE

    await db.commit()
    await db.refresh(campaign)

    return CampaignResponse.model_validate(campaign)

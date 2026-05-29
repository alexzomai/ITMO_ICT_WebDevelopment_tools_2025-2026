from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.connection import get_session
from notifications.models import (
    Notification,
    NotificationCreate,
    NotificationRead,
    NotificationUpdate,
)

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("/", response_model=List[NotificationRead])
async def notifications_list(session: AsyncSession = Depends(get_session)) -> List[NotificationRead]:
    return (await session.exec(select(Notification))).all()


@router.get("/{notification_id}", response_model=NotificationRead)
async def notification_get(notification_id: int, session: AsyncSession = Depends(get_session)) -> NotificationRead:
    db_notification = await session.get(Notification, notification_id)
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return db_notification


@router.post("/", status_code=201, response_model=NotificationRead)
async def notification_create(
    notification: NotificationCreate, session: AsyncSession = Depends(get_session)
) -> NotificationRead:
    db_notification = Notification.model_validate(notification)
    session.add(db_notification)
    await session.commit()
    await session.refresh(db_notification)
    return db_notification


@router.patch("/{notification_id}", response_model=NotificationRead)
async def notification_update(
    notification_id: int,
    notification: NotificationUpdate,
    session: AsyncSession = Depends(get_session),
) -> NotificationRead:
    db_notification = await session.get(Notification, notification_id)
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    for key, value in notification.model_dump(exclude_unset=True).items():
        setattr(db_notification, key, value)
    session.add(db_notification)
    await session.commit()
    await session.refresh(db_notification)
    return db_notification


@router.delete("/{notification_id}", status_code=204)
async def notification_delete(notification_id: int, session: AsyncSession = Depends(get_session)) -> None:
    db_notification = await session.get(Notification, notification_id)
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    await session.delete(db_notification)
    await session.commit()
